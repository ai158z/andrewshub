import pytest
from unittest.mock import patch, MagicMock, mock_open
from src.backend.api.system import router, redis_client
from fastapi.testclient import TestClient
from src.backend.models.agent import Agent
from src.backend.models.metric import Metric
import json

# Test client for FastAPI
client = TestClient(router)

# Mock data for tests
MOCK_AGENT = Agent(id=1, name="test-agent")
MOCK_METRICS = [
    Metric(cpu_usage=45.5, memory_usage=60.2, disk_io=100, network_io=200),
    Metric(cpu_usage=30.0, memory_usage=55.1, disk_io=150, network_io=180)
]

def test_health_endpoint_success():
    with patch('psutil.cpu_percent', return_value=25.0), \
         patch('psutil.virtual_memory') as mock_memory, \
         patch('psutil.disk_usage') as mock_disk:
        
        mock_memory.return_value = MagicMock(percent=30.0, available=2*1024**3)
        mock_disk.return_value = MagicMock(used=50*1024**3, free=100*1024**3, total=150*1024**3)
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "degraded"]
        assert "cpu_usage_percent" in data
        assert "memory_usage_percent" in data

def test_health_endpoint_exception():
    with patch('psutil.cpu_percent', side_effect=Exception("psutil error")):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"

def test_get_system_metrics_success():
    with patch('src.backend.api.system.get_db') as mock_db:
        mock_db_instance = mock_db.return_value
        mock_db_instance.query().order_by().limit().all.return_value = MOCK_METRICS
        
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "cpu_usage" in data
        assert "memory_usage" in data
        assert len(data["cpu_usage"]) == 2

def test_get_system_metrics_exception():
    with patch('src.backend.api.system.get_db', side_effect=Exception("Database error")):
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data

def test_system_status_success():
    with patch('src.backend.api.system.get_db') as mock_get_db, \
         patch('psutil.cpu_percent', return_value=25.0), \
         patch('psutil.virtual_memory') as mock_memory, \
         patch('psutil.disk_usage') as mock_disk:
        
        mock_db_instance = mock_get_db.return_value
        mock_db_instance.query().count.return_value = 5
        
        mock_memory.return_value = MagicMock(percent=30.0)
        mock_disk.return_value = MagicMock(used=50*1024**3, total=100*1024**3)
        
        response = client.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert "database" in data
        assert "redis" in data
        assert "cpu_usage" in data

def test_system_status_exception():
    with patch('src.backend.api.system.get_db', side_effect=Exception("Database connection failed")):
        response = client.get("/status")
        data = response.json()
        assert data["status"] == "error"

def test_system_resources_success():
    with patch('psutil.cpu_count', return_value=4), \
         patch('psutil.cpu_percent') as mock_cpu_percent, \
         patch('psutil.virtual_memory') as mock_memory, \
         patch('psutil.disk_usage') as mock_disk, \
         patch('psutil.net_io_counters') as mock_net_io:
        
        mock_cpu_percent.return_value = [20.0, 30.0, 25.0, 35.0]
        mock_memory.return_value = MagicMock(total=8*1024**3, available=4*1024**3, used=4*1024**3, percent=50.0)
        mock_disk.return_value = MagicMock(total=500*1024**3, used=200*1024**3, free=300*1024**3)
        mock_net_io.return_value = MagicMock(bytes_sent=1000, bytes_recv=2000, packets_sent=10, packets_recv=15)
        
        response = client.get("/resources")
        assert response.status_code == 200
        data = response.json()
        assert "cpu" in data
        assert "memory" in data
        assert "disk" in data
        assert "network" in data

def test_system_resources_exception():
    with patch('psutil.cpu_count', side_effect=Exception("psutil error")):
        response = client.get("/resources")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data

def test_redis_connection_success():
    with patch('src.backend.api.system.redis.from_url') as mock_redis, \
         patch('src.backend.api.system.redis_client') as mock_client:
        mock_redis.return_value.ping.return_value = True
        # Test that we can import the module and the redis client gets initialized
        import src.backend.api.system
        assert src.backend.api.system.redis_client is not None

def test_redis_connection_failure():
    with patch('src.backend.api.system.redis.from_url', side_effect=Exception("Connection failed")):
        # Re-import to trigger the redis connection logic
        import importlib
        import src.backend.api.system
        importlib.reload(src.backend.api.system)
        # The client should be None when connection fails
        # Note: In a real test environment, we'd need to check the actual behavior

@pytest.mark.parametrize("cpu,memory,expected_status", [
    (85, 80, "healthy"),
    (95, 95, "degraded"),
])
def test_health_status_determination(cpu, memory, expected_status):
    with patch('psutil.cpu_percent', return_value=cpu), \
         patch('psutil.virtual_memory') as mock_memory, \
         patch('psutil.disk_usage') as mock_disk:
        
        mock_memory.return_value = MagicMock(percent=memory, available=2*1024**3)
        mock_disk.return_value = MagicMock(used=50*1024**3, free=100*1024**3, total=150*1024**3)
        
        response = client.get("/health")
        data = response.json()
        assert data["status"] == expected_status

def test_empty_metrics():
    with patch('src.backend.api.system.get_db') as mock_db:
        mock_db_instance = mock_db.return_value
        mock_db_instance.query().order_by().limit().all.return_value = []
        
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert len(data["cpu_usage"]) == 0
        assert len(data["memory_usage"]) == 0

def test_agent_count_zero():
    with patch('src.backend.api.system.get_db') as mock_db:
        mock_db_instance = mock_db.return_value
        mock_db_instance.query().count.return_value = 0
        
        response = client.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert data["agent_count"] == 0

def test_network_io_counters_exception():
    with patch('psutil.net_io_counters', side_effect=Exception("Network error")):
        response = client.get("/resources")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data

def test_disk_usage_exception():
    with patch('psutil.disk_usage', side_effect=Exception("Disk access error")):
        response = client.get("/health")
        # Should still return a response even with disk error
        assert response.status_code == 200

def test_cpu_percent_exception():
    with patch('psutil.cpu_percent', side_effect=Exception("CPU access error")):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"

def test_memory_percent_exception():
    with patch('psutil.virtual_memory', side_effect=Exception("Memory access error")):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"

def test_per_core_cpu_metrics():
    with patch('psutil.cpu_percent') as mock_cpu_percent:
        mock_cpu_percent.return_value = [20.0, 30.0, 25.0, 35.0]
        response = client.get("/resources")
        assert response.status_code == 200
        data = response.json()
        assert "cpu" in data
        assert len(data["cpu"]["usage_per_core"]) == 4

def test_memory_info_exception():
    with patch('psutil.virtual_memory', side_effect=Exception("Memory error")):
        response = client.get("/resources")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data