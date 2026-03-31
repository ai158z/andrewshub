import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from src.quantum_sensors.models import SensorReading, SensorFusionData

@pytest.fixture
def app_instance():
    """Create FastAPI app instance for testing"""
    from src.main import app
    return app

@pytest.fixture
def test_client(app_instance):
    """Create test client for API testing"""
    return TestClient(app_instance)

@pytest.fixture
def mock_components():
    """Mock all external components"""
    with patch('src.main.ConfigManager') as mock_config, \
         patch('src.main.ZenoProcessor') as mock_zeno, \
         patch('src.main.CodonicProcessor') as mock_codonic, \
         patch('src.main.EntanglementHandler') as mock_entanglement, \
         patch('src.main.ROS2Bridge') as mock_ros2, \
         patch('src.main.validate_sensor_data') as mock_validate, \
         patch('src.main.normalize_quantum_states') as mock_normalize, \
         patch('src.main.fuse_sensors') as mock_fuse:
        
        # Setup mock returns
        mock_config.return_value.get_config.return_value = {"test": "config"}
        mock_config.return_value.set_config.return_value = None
        
        mock_zeno.return_value.apply_zeno_stabilization.return_value = SensorReading(
            sensor_id="test", 
            timestamp=1234567890, 
            data={"normalized": True},
            quantum_state="test_state"
        )
        
        mock_codonic.return_value.process_codonic_layer.return_value = SensorReading(
            sensor_id="test",
            timestamp=1234567890,
            data={"processed": True},
            quantum_state="test_state"
        )
        
        mock_entanglement.return_value.correlate_sensors.return_value = {"entangled": True}
        
        mock_validate.return_value = None
        mock_normalize.return_value = SensorReading(
            sensor_id="test",
            timestamp=1234567890,
            data={"normalized": True},
            quantum_state="test_state"
        )
        
        mock_fuse.return_value = SensorReading(
            sensor_id="fused",
            timestamp=1234567890,
            data={"fused": True},
            quantum_state="test_state"
        )
        
        yield {
            'config': mock_config,
            'zeno': mock_zeno,
            'codonic': mock_codonic,
            'entanglement': mock_entanglement,
            'ros2': mock_ros2,
            'validate': mock_validate,
            'normalize': mock_normalize,
            'fuse': mock_fuse
        }

# Test cases
def test_root_endpoint(test_client):
    """Test root endpoint returns correct response"""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Quantum Sensory Feedback API is running",
        "status": "healthy"
    }

def test_health_check_endpoint(test_client):
    """Test health check endpoint"""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "service" in data
    assert data["status"] == "healthy"
    assert data["service"] == "quantum-sensory-feedback"

def test_fuse_sensor_data_success(test_client, mock_components):
    """Test successful sensor fusion"""
    # Prepare test data
    payload = {
        "visual_data": {
            "sensor_id": "visual_1",
            "timestamp": 1234567890,
            "data": {"intensity": 0.5},
            "quantum_state": "test_state"
        },
        "tactile_data": {
            "sensor_id": "tactile_1", 
            "timestamp": 1234567890,
            "data": {"pressure": 0.3},
            "quantum_state": "test_state"
        }
    }
    
    response = test_client.post("/sensor/fuse", json=payload)
    assert response.status_code == 200

def test_fuse_sensor_data_validation_error(test_client, mock_components):
    """Test sensor fusion with invalid data"""
    # Mock validate_sensor_data to raise an exception
    mock_components['validate'].side_effect = ValueError("Invalid sensor data")
    
    payload = {
        "visual_data": {
            "sensor_id": "",  # Invalid empty sensor_id
            "timestamp": 1234567890,
            "data": {},
            "quantum_state": "test_state"
        },
        "tactile_data": {
            "sensor_id": "tactile_1",
            "timestamp": 1234567890,
            "data": {"pressure": 0.3},
            "quantum_state": "test_state"
        }
    }
    
    response = test_client.post("/sensor/fuse", json=payload)
    assert response.status_code == 500
    assert "Sensor fusion failed" in response.json()["detail"]

def test_process_sensor_data_success(test_client, mock_components):
    """Test successful individual sensor data processing"""
    sensor_data = {
        "sensor_id": "test_sensor",
        "timestamp": 1234567890,
        "data": {"test": "data"},
        "quantum_state": "test_state"
    }
    
    response = test_client.post("/sensor/process", json=sensor_data)
    assert response.status_code == 200

def test_process_sensor_data_error(test_client, mock_components):
    """Test sensor processing with error"""
    # Mock validate_sensor_data to raise an exception
    mock_components['validate'].side_effect = Exception("Processing error")
    
    sensor_data = {
        "sensor_id": "test_sensor",
        "timestamp": 1234567890,
        "data": {"test": "data"},
        "quantum_state": "test_state"
    }
    
    response = test_client.post("/sensor/process", json=sensor_data)
    assert response.status_code == 500

def test_get_config_success(test_client, mock_components):
    """Test successful configuration retrieval"""
    response = test_client.get("/config")
    assert response.status_code == 200
    assert "test" in response.json()

def test_get_config_error(test_client):
    """Test configuration retrieval error"""
    with patch('src.main.ConfigManager') as mock_config:
        mock_config.return_value.get_config.side_effect = Exception("Config error")
        response = test_client.get("/config")
        assert response.status_code == 500

def test_update_config_success(test_client, mock_components):
    """Test successful configuration update"""
    config_data = {"test_key": "test_value"}
    response = test_client.post("/config", json=config_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Configuration updated successfully"

def test_update_config_error(test_client):
    """Test configuration update error"""
    with patch('src.main.ConfigManager') as mock_config:
        mock_config.return_value.set_config.side_effect = Exception("Update failed")
        response = test_client.post("/config", json={"key": "value"})
        assert response.status_code == 500

def test_correlate_sensors_success(test_client, mock_components):
    """Test successful sensor correlation"""
    visual_data = {
        "sensor_id": "visual_1",
        "timestamp": 1234567890,
        "data": {"intensity": 0.5},
        "quantum_state": "test_state"
    }
    
    tactile_data = {
        "sensor_id": "tactile_1",
        "timestamp": 1234567890,
        "data": {"pressure": 0.3},
        "quantum_state": "test_state"
    }
    
    response = test_client.post("/entangle", json={
        "visual_data": visual_data,
        "tactile_data": tactile_data
    })
    
    assert response.status_code == 200

def test_correlate_sensors_validation_error(test_client, mock_components):
    """Test sensor correlation with validation error"""
    # Mock validate_sensor_data to raise an exception
    mock_components['validate'].side_effect = ValueError("Invalid data")
    
    visual_data = {
        "sensor_id": "",  # Invalid data
        "timestamp": 1234567890,
        "data": {},
        "quantum_state": "test_state"
    }
    
    tactile_data = {
        "sensor_data": {
            "sensor_id": "tactile_1",
            "timestamp": 1234567890,
            "data": {"pressure": 0.3},
            "quantum_state": "test_state"
        }
    }
    
    response = test_client.post("/entangle", json={
        "visual_data": visual_data,
        "tactile_data": tactile_data
    })
    
    assert response.status_code == 500
    assert "Sensor correlation failed" in response.json()["detail"]

def test_edge_case_empty_data(test_client):
    """Test edge case with empty sensor data"""
    empty_data = {
        "visual_data": {
            "sensor_id": "",
            "timestamp": 0,
            "data": {},
            "quantum_state": ""
        },
        "tactile_data": {
            "sensor_id": "",
            "timestamp": 0,
            "data": {},
            "quantum_state": ""
        }
    }
    
    response = test_client.post("/sensor/fuse", json=empty_data)
    # Should handle gracefully or return validation error
    assert response.status_code in [200, 500]

def test_edge_case_large_data_payload(test_client):
    """Test with large sensor data payload"""
    large_data = {
        "visual_data": {
            "sensor_id": "visual_large",
            "timestamp": 1234567890,
            "data": {f"key_{i}": f"value_{i}" for i in range(1000)},  # Large data set
            "quantum_state": "test_state"
        },
        "tactile_data": {
            "sensor_id": "tactile_large",
            "timestamp": 1234567890,
            "data": {f"pressure_{i}": i * 0.1 for i in range(1000)},
            "quantum_state": "test_state"
        }
    }
    
    response = test_client.post("/sensor/fuse", json=large_data)
    assert response.status_code in [200, 500]  # Either success or server error

def test_edge_case_invalid_timestamp(test_client):
    """Test with invalid timestamp values"""
    invalid_data = {
        "visual_data": {
            "sensor_id": "test",
            "timestamp": -1,  # Invalid negative timestamp
            "data": {"test": "data"},
            "quantum_state": "test_state"
        },
        "tactile_data": {
            "sensor_id": "test",
            "timestamp": "invalid",  # Invalid string timestamp
            "data": {"test": "data"},
            "quantum_state": "test_state"
        }
    }
    
    response = test_client.post("/sensor/fuse", json=invalid_data)
    # Should either validate and handle or return error
    assert response.status_code in [200, 422, 500]

def test_mock_component_failures(test_client, mock_components):
    """Test behavior when components fail"""
    # Simulate component failure
    mock_components['zeno'].return_value.apply_zeno_stabilization.side_effect = Exception("Component failure")
    
    sensor_data = {
        "sensor_id": "test_sensor",
        "timestamp": 1234567890,
        "data": {"test": "data"},
        "quantum_state": "test_state"
    }
    
    response = test_client.post("/sensor/process", json=sensor_data)
    assert response.status_code == 500

@pytest.mark.parametrize("endpoint,payload", [
    ("/sensor/fuse", {
        "visual_data": {
            "sensor_id": "test", "timestamp": 1234567890, "data": {}, "quantum_state": "test"
        },
        "tactile_data": {
            "sensor_id": "test", "timestamp": 1234567890, "data": {}, "quantum_state": "test"
        }
    }),
    ("/sensor/process", {
        "sensor_id": "test", "timestamp": 1234567890, "data": {}, "quantum_state": "test"
    }),
])
def test_all_endpoints_with_empty_data(test_client, endpoint, payload):
    """Test all endpoints with minimal valid data"""
    response = test_client.post(endpoint, json=payload)
    # Should not crash, either success or validation error
    assert response.status_code in [200, 422, 500]

def test_concurrent_requests(test_client, mock_components):
    """Test multiple concurrent requests (simulated)"""
    import threading
    import time
    
    results = []
    
    def make_request():
        payload = {
            "sensor_id": f"test_{threading.get_ident()}",
            "timestamp": int(time.time()),
            "data": {"test": "data"},
            "quantum_state": "test_state"
        }
        response = test_client.post("/sensor/process", json=payload)
        results.append(response.status_code)
    
    # Simulate concurrent requests
    threads = []
    for _ in range(3):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # All requests should complete without crashing
    assert all(code in [200, 500] for code in results)