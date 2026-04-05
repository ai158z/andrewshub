import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.agent_service import get_all_agents, get_agent_by_id, update_agent, get_agent_status_service
from app.models.agent import Agent
from app.schemas.agent import AgentUpdate

def test_get_all_agents_success():
    db = MagicMock(spec=Session)
    agents = [MagicMock(spec=Agent), MagicMock(spec=Agent)]
    db.query().all.return_value = agents
    
    result = get_all_agents(db)
    
    assert result == agents
    db.query.assert_called_once_with(Agent)
    db.query().all.assert_called_once()

def test_get_all_agents_db_error():
    db = MagicMock(spec=Session)
    db.query().all.side_effect = Exception("DB error")
    
    with pytest.raises(HTTPException) as exc_info:
        get_all_agents(db)
    
    assert exc_info.value.status_code == 500
    assert "Failed to retrieve agents" in exc_info.value.detail

def test_get_agent_by_id_success():
    db = MagicMock(spec=Session)
    agent = MagicMock(spec=Agent)
    agent.id = 1
    db.query().filter().first.return_value = agent
    
    result = get_agent_by_id(db, 1)
    
    assert result == agent

def test_get_agent_by_id_not_found():
    db = MagicMock(spec=Session)
    db.query().filter().first.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        get_agent_by_id(db, 999)
    
    assert exc_info.value.status_code == 404

def test_get_agent_by_id_db_error():
    db = MagicMock(spec=Session)
    db.query().filter().first.side_effect = Exception("DB error")
    
    with pytest.raises(HTTPException) as exc_info:
        get_agent_by_id(db, 1)
    
    assert exc_info.value.status_code == 500

def test_update_agent_success():
    db = MagicMock(spec=Session)
    agent = MagicMock(spec=Agent)
    agent.id = 1
    db.query().filter().first.return_value = agent
    
    update_data = AgentUpdate(name="Updated Agent")
    result = update_agent(db, 1, update_data)
    
    assert result == agent
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(agent)

def test_update_agent_not_found():
    db = MagicMock(spec=Session)
    db.query().filter().first.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        update_agent(db, 999, AgentUpdate(name="Test"))
    
    assert exc_info.value.status_code == 404

def test_update_agent_db_error():
    db = MagicMock(spec=Session)
    agent = MagicMock(spec=Agent)
    agent.id = 1
    db.query().filter().first.return_value = agent
    db.commit.side_effect = Exception("DB error")
    
    with pytest.raises(HTTPException) as exc_info:
        update_agent(db, 1, AgentUpdate(name="Test"))
    
    assert exc_info.value.status_code == 500

def test_get_agent_status_service_success():
    with patch("app.services.agent_service.get_agent_status") as mock_status:
        mock_status.return_value = {"status": "active"}
        result = get_agent_status_service(1)
        
    assert result == {"status": "active"}

def test_get_agent_status_service_ros2_error():
    with patch("app.services.agent_service.get_agent_status", side_effect=Exception("ROS2 error")):
        with pytest.raises(HTTPException) as exc_info:
            get_agent_status_service(1)
    
    assert exc_info.value.status_code == 500
    assert "Failed to retrieve agent status" in exc_info.value.detail