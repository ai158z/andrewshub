import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from fastapi import HTTPException
from src.backend.api.agents import (
    register_agent, update_agent_status, agent_heartbeat, get_agent, 
    list_agents, record_metrics, get_agent_metrics, get_agent_health
)
from src.backend.schemas.agent import AgentCreate
from src.backend.schemas.metric import MetricCreate

# Test fixtures
@pytest.fixture
def mock_db():
    with patch('src.backend.api.agents.get_db') as mock:
        yield mock.return_value

@pytest.fixture
def sample_agent_create():
    return AgentCreate(
        agent_id="test-agent-001",
        name="Test Agent",
        status="active"
    )

@pytest.fixture
def sample_metric_create():
    return [
        MetricCreate(
            metric_name="cpu_usage",
            value=75.5,
            timestamp=datetime.utcnow()
        )
    ]

def test_register_agent_success(mock_db, sample_agent_create):
    # Setup
    db_agent = MagicMock()
    db_agent.agent_id = sample_agent_create.agent_id
    db_agent.name = sample_agent_create.name
    db_agent.status = sample_agent_create.status
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=db_agent)
    
    # Execute
    result = register_agent(sample_agent_create, mock_db)
    
    # Assert
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    assert result.agent_id == sample_agent_create.agent_id
    assert result.name == sample_agent_create.name

def test_register_agent_db_error(mock_db, sample_agent_create):
    # Setup
    mock_db.add.side_effect = Exception("DB error")
    
    # Assert
    with pytest.raises(HTTPException) as exc_info:
        register_agent(sample_agent_create, mock_db)
    assert exc_info.value.status_code == 500

def test_update_agent_status_success(mock_db):
    # Setup
    agent = MagicMock()
    agent.agent_id = "test-agent"
    agent.status = "active"
    mock_db.query().filter().first.return_value = agent
    
    # Execute
    result = update_agent_status("test-agent", "inactive", mock_db)
    
    # Assert
    assert result["message"] == "Agent test-agent status updated to inactive"
    mock_db.commit.assert_called_once()

def test_update_agent_status_not_found(mock_db):
    # Setup
    mock_db.query().filter().first.return_value = None
    
    # Assert
    with pytest.raises(HTTPException) as exc_info:
        update_agent_status("nonexistent", "inactive", mock_db)
    assert exc_info.value.status_code == 404

def test_update_agent_status_db_error(mock_db):
    # Setup
    agent = MagicMock()
    agent.agent_id = "test-agent"
    mock_db.query().filter().first.return_value = agent
    mock_db.commit.side_effect = Exception("DB error")
    
    # Assert
    with pytest.raises(HTTPException) as exc_info:
        update_agent_status("test-agent", "inactive", mock_db)
    assert exc_info.value.status_code == 500

def test_agent_heartbeat_success(mock_db):
    # Setup
    agent = MagicMock()
    agent.agent_id = "test-agent"
    mock_db.query().filter().first.return_value = agent
    
    # Execute
    result = agent_heartbeat("test-agent", mock_db)
    
    # Assert
    assert result["message"] == "Heartbeat recorded"
    mock_db.commit.assert_called_once()

def test_agent_heartbeat_not_found(mock_db):
    # Setup
    mock_db.query().filter().first.return_value = None
    
    # Assert
    with pytest.raises(HTTPException) as exc_info:
        agent_heartbeat("nonexistent", mock_db)
    assert exc_info.value.status_code == 404

def test_get_agent_success(mock_db):
    # Setup
    agent = MagicMock()
    agent.agent_id = "test-agent"
    agent.name = "Test Agent"
    mock_db.query().filter().first.return_value = agent
    
    # Execute
    result = get_agent("test-agent", mock_db)
    
    # Assert
    assert result.agent_id == "test-agent"
    assert result.name == "Test Agent"

def test_get_agent_not_found(mock_db):
    # Setup
    mock_db.query().filter().first.return_value = None
    
    # Assert
    with pytest.raises(HTTPException) as exc_info:
        get_agent("nonexistent", mock_db)
    assert exc_info.value.status_code == 404

def test_list_agents_success(mock_db):
    # Setup
    agent1 = MagicMock()
    agent1.agent_id = "agent-1"
    agent2 = MagicMock()
    agent2.agent_id = "agent-2"
    mock_db.query().all.return_value = [agent1, agent2]
    
    # Execute
    result = list_agents(mock_db)
    
    # Assert
    assert len(result) == 2
    mock_db.query().all.assert_called_once()

def test_list_agents_db_error(mock_db):
    # Setup
    mock_db.query().all.side_effect = Exception("DB error")
    
    # Assert
    with pytest.raises(HTTPException) as exc_info:
        list_agents(mock_db)
    assert exc_info.value.status_code == 500

def test_record_metrics_success(mock_db, sample_metric_create):
    # Setup
    agent = MagicMock()
    agent.agent_id = "test-agent"
    mock_db.query().filter().first.return_value = agent
    
    # Execute
    result = record_metrics("test-agent", sample_metric_create, mock_db)
    
    # Assert
    assert result["message"] == "Metrics recorded"
    mock_db.commit.assert_called_once()

def test_record_metrics_agent_not_found(mock_db, sample_metric_create):
    # Setup
    mock_db.query().filter().first.return_value = None
    
    # Assert
    with pytest.raises(HTTPException) as exc_info:
        record_metrics("nonexistent", sample_metric_create, mock_db)
    assert exc_info.value.status_code == 404

def test_get_agent_metrics_success(mock_db):
    # Setup
    agent = MagicMock()
    agent.agent_id = "test-agent"
    mock_db.query().filter().first.return_value = agent
    mock_db.query().filter().all.return_value = []
    
    # Execute
    result = get_agent_metrics("test-agent", mock_db)
    
    # Assert
    assert isinstance(result, list)
    mock_db.query().filter().all.assert_called_once()

def test_get_agent_metrics_agent_not_found(mock_db):
    # Setup
    mock_db.query().filter().first.return_value = None
    
    # Assert
    with pytest.raises(HTTPException) as exc_info:
        get_agent_metrics("nonexistent", mock_db)
    assert exc_info.value.status_code == 404

def test_get_agent_health_success(mock_db):
    # Setup
    agent1 = MagicMock()
    agent1.agent_id = "agent-1"
    agent1.name = "Agent 1"
    agent1.status = "active"
    agent1.last_heartbeat = datetime.utcnow()
    
    agent2 = MagicMock()
    agent2.agent_id = "agent-2"
    agent2.name = "Agent 2"
    agent2.status = "inactive"
    agent2.last_heartbeat = datetime.utcnow() - timedelta(minutes=10)
    
    mock_db.query().all.return_value = [agent1, agent2]
    
    # Execute
    result = get_agent_health(mock_db)
    
    # Assert
    assert result["total_agents"] == 2
    mock_db.query().all.assert_called_once()

def test_get_agent_health_db_error(mock_db):
    # Setup
    mock_db.query().all.side_effect = Exception("DB error")
    
    # Assert
    with pytest.raises(HTTPException) as exc_info:
        get_agent_health(mock_db)
    assert exc_info.value.status_code == 500

def test_register_agent_empty_fields(mock_db):
    # Setup
    agent_create = AgentCreate(
        agent_id="",  # Empty agent_id
        name="",     # Empty name
        status="active"
    )
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
    
    # Execute
    result = register_agent(agent_create, mock_db)
    
    # Assert
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    assert result.agent_id == ""
    assert result.name == ""

def test_agent_heartbeat_no_agent(mock_db):
    # Setup
    mock_db.query().filter().first.return_value = None
    
    # Assert
    with pytest.raises(HTTPException) as exc_info:
        agent_heartbeat("nonexistent", mock_db)
    assert exc_info.value.status_code == 404

def test_record_metrics_empty_list(mock_db):
    # Setup
    agent = MagicMock()
    agent.agent_id = "test-agent"
    mock_db.query().filter().first.return_value = agent
    mock_db.commit = MagicMock()
    
    # Execute
    metrics = []  # Empty metrics list
    result = record_metrics("test-agent", metrics, mock_db)
    
    # Assert
    assert result["message"] == "Metrics recorded"
    # Should not call db.add since metrics list is empty
    mock_db.add.assert_not_called()
    mock_db.commit.assert_called_once()