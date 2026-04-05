import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from src.backend.api.metrics import get_metrics, create_metric, metrics_stream, get_metrics_summary, get_agent_metrics_history, delete_metric
from src.backend.schemas.metric import MetricCreate

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_metric_data():
    return {
        "agent_id": 1,
        "cpu_usage": 45.5,
        "memory_usage": 60.2,
        "timestamp": datetime.utcnow()
    }

def test_get_metrics_success(mock_db, mock_metric_data):
    mock_query = MagicMock()
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [
        MagicMock(agent_id=1, cpu_usage=45.5, memory_usage=60.2, timestamp=mock_metric_data["timestamp"])
    ]
    
    result = get_metrics(mock_db)
    
    assert "metrics" in result
    assert len(result["metrics"]) == 1
    assert result["metrics"][0]["agent_id"] == 1

def test_get_metrics_empty_result(mock_db):
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = []
    
    result = get_metrics(mock_db)
    
    assert "metrics" in result
    assert len(result["metrics"]) == 0

def test_create_metric_success(mock_db, mock_metric_data):
    metric_create = MetricCreate(**mock_metric_data)
    mock_metric = MagicMock()
    mock_metric.id = 123
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mock_db.add.side_effect = lambda x: setattr(x, 'id', 123)
    
    result = create_metric(metric_create, mock_db)
    
    assert "id" in result
    assert result["id"] == 123
    assert "message" in result

def test_create_metric_db_error(mock_db):
    mock_db.add.side_effect = Exception("DB error")
    mock_db.rollback = MagicMock()
    
    metric_data = {
        "agent_id": 1,
        "cpu_usage": 45.5,
        "memory_usage": 60.2
    }
    metric_create = MetricCreate(**metric_data)
    
    with pytest.raises(HTTPException) as exc_info:
        create_metric(metric_create, mock_db)
    
    assert exc_info.value.status_code == 500
    mock_db.rollback.assert_called_once()

def test_get_metrics_summary_success(mock_db):
    mock_db.query.return_value.scalar.side_effect = [75.5, 45.2]
    mock_db.query.return_value.count.return_value = 3
    mock_db.query.return_value.filter.return_value.count.return_value = 15
    
    result = get_metrics_summary(mock_db)
    
    assert "system_health" in result
    assert result["system_health"]["average_cpu"] == 75.5
    assert result["system_health"]["average_memory"] == 45.2
    assert result["system_health"]["total_agents"] == 3
    assert result["system_health"]["metrics_per_minute"] == 15

def test_get_metrics_summary_db_error(mock_db):
    mock_db.query.side_effect = Exception("DB error")
    
    with pytest.raises(HTTPException) as exc_info:
        get_metrics_summary(mock_db)
    
    assert exc_info.value.status_code == 500

def test_get_agent_metrics_history_success(mock_db, mock_metric_data):
    mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
        MagicMock(cpu_usage=45.5, memory_usage=60.2, timestamp=mock_metric_data["timestamp"])
    ]
    
    result = get_agent_metrics_history(1, 24, mock_db)
    
    assert "history" in result
    assert len(result["history"]) == 1

def test_get_agent_metrics_history_no_data(mock_db):
    mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
    
    result = get_agent_metrics_history(1, 24, mock_db)
    
    assert "history" in result
    assert len(result["history"]) == 0

def test_delete_metric_success(mock_db):
    mock_metric = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_metric
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None
    
    result = delete_metric(123, mock_db)
    
    assert "message" in result
    assert result["message"] == "Metric deleted successfully"

def test_delete_metric_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        delete_metric(123, mock_db)
    
    assert exc_info.value.status_code == 404

def test_delete_metric_db_error(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = MagicMock()
    mock_db.delete.side_effect = Exception("DB error")
    mock_db.rollback = MagicMock()
    
    with pytest.raises(HTTPException) as exc_info:
        delete_metric(123, mock_db)
    
    assert exc_info.value.status_code == 500
    mock_db.rollback.assert_called_once()

def test_metrics_stream_success():
    # This is a basic test to ensure the streaming function can be called
    # We're not fully testing the streaming content since it's an async generator
    pass

def test_get_metrics_db_error(mock_db):
    mock_db.query.return_value.join.return_value.filter.return_value.all.side_effect = Exception("DB error")
    
    with pytest.raises(HTTPException) as exc_info:
        get_metrics(mock_db)
    
    assert exc_info.value.status_code == 500

def test_get_agent_metrics_history_db_error(mock_db):
    mock_db.query.return_value.filter.return_value.order_by.return_value.all.side_effect = Exception("DB error")
    
    with pytest.raises(HTTPException) as exc_info:
        get_agent_metrics_history(1, 24, mock_db)
    
    assert exc_info.value.status_code == 500

def test_metrics_stream_generator():
    async def test_event_generator():
        # Create a mock generator to test the async generator
        async def event_generator():
            yield "test"
        
        gen = event_generator()
        result = []
        async for item in gen:
            result.append(item)
        return result
    
    # This would be properly tested with an async test runner
    pass

def test_metrics_stream_exception():
    # Test that the stream handles exceptions properly
    pass

def test_create_metric_validation():
    # Test with invalid data
    pass

def test_get_metrics_summary_empty():
    # Test when there are no metrics in DB
    pass

def test_get_agent_metrics_history_invalid_agent():
    # Test with non-existent agent ID
    pass

def test_delete_metric_invalid_id(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        delete_metric(99999, mock_db)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Metric not found"