import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock
from typing import List
from backend.app.api.routes.agents import router
from backend.app.schemas.agent import AgentBase

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_agents():
    return [
        {"id": 1, "name": "Agent1", "status": "active"},
        {"id": 2, "name": "Agent2", "status": "inactive"}
    ]

def test_get_agents_success(mock_db, mock_agents):
    with patch("backend.app.api.routes.agents.get_all_agents", return_value=mock_agents):
        response = router.get("/", response_model=List[AgentBase])(lambda db: mock_agents)(db=mock_db)
        assert response == mock_agents

def test_get_agents_exception_handling(mock_db):
    with patch("backend.app.api.routes.agents.get_all_agents", side_effect=Exception("DB Error")):
        with pytest.raises(HTTPException) as exc_info:
            router.get("/", response_model=List[AgentBase])(lambda db: [])(db=mock_db)
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Failed to retrieve agents"

def test_get_agent_success(mock_db):
    agent_data = {"id": 1, "name": "Test Agent", "status": "active"}
    with patch("backend.app.api.routes.agents.get_agent_by_id", return_value=agent_data):
        response = router.get("/{agent_id}", response_model=AgentBase)(lambda agent_id, db: agent_data)(agent_id=1, db=mock_db)
        assert response["id"] == 1

def test_get_agent_not_found(mock_db):
    with patch("backend.app.api.routes.agents.get_agent_by_id", return_value=None):
        with pytest.raises(HTTPException) as exc_info:
            router.get("/{agent_id}", response_model=AgentBase)(lambda agent_id, db: None)(agent_id=999, db=mock_db)
        assert exc_info.value.status_code == 404

def test_get_agent_exception_handling(mock_db):
    with patch("backend.app.api.routes.agents.get_agent_by_id", side_effect=Exception("DB Error")):
        with pytest.raises(HTTPException) as exc_info:
            router.get("/{agent_id}", response_model=AgentBase)(lambda agent_id, db: {})(agent_id=1, db=mock_db)
        assert exc_info.value.status_code == 500

def test_update_agent_status_success(mock_db):
    updated_agent = {"id": 1, "name": "Test Agent", "status": "updated"}
    with patch("backend.app.api.routes.agents.update_agent", return_value=updated_agent):
        response = router.put("/{agent_id}/status")(lambda agent_id, status, db: status)(agent_id=1, status={"status": "active"}, db=mock_db)
        assert response["status"] == "active"

def test_update_agent_not_found(mock_db):
    with patch("backend.app.api.routes.agents.update_agent", return_value=None):
        with pytest.raises(HTTPException) as exc_info:
            router.put("/{agent_id}/status")(lambda agent_id, status, db: None)(agent_id=999, status={}, db=mock_db)
        assert exc_info.value.status_code == 404

def test_update_agent_exception_handling(mock_db):
    with patch("backend.app.api.routes.agents.update_agent", side_effect=Exception("Update failed")):
        with pytest.raises(HTTPException) as exc_info:
            router.put("/{agent_id}/status")(lambda agent_id, status, db: {})(agent_id=1, status={}, db=mock_db)
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Failed to update agent status"

def test_get_agent_status_from_ros2(mock_db):
    with patch("backend.app.api.routes.agents.ros2_get_agent_status", return_value={"status": "ros2_status"}):
        response = router.get("/{agent_id}/status")(lambda agent_id, db: {})(agent_id=1, db=mock_db)
        assert response == {"status": "ros2_status"}

def test_get_agent_status_fallback_to_db(mock_db):
    agent_data = {"id": 1, "name": "Test Agent", "status": "active"}
    with patch("backend.app.api.routes.agents.ros2_get_agent_status", return_value=None):
        with patch("backend.app.api.routes.agents.get_agent_by_id", return_value=agent_data):
            response = router.get("/{agent_id}/status")(lambda agent_id, db: {})(agent_id=1, db=mock_db)
            assert response == agent_data

def test_get_agent_status_agent_not_found(mock_db):
    with patch("backend.app.api.routes.agents.ros2_get_agent_status", return_value=None):
        with patch("backend.app.api.routes.agents.get_agent_by_id", return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                router.get("/{agent_id}/status")(lambda agent_id, db: {})(agent_id=1, db=mock_db)
            assert exc_info.value.status_code == 404

def test_get_agent_status_exception_handling(mock_db):
    with patch("backend.app.api.routes.agents.ros2_get_agent_status", side_effect=Exception("Status error")):
        with patch("backend.app.api.routes.agents.get_agent_by_id", side_effect=Exception("DB Error")):
            with pytest.raises(HTTPException) as exc_info:
                router.get("/{agent_id}/status")(lambda agent_id, db: {})(agent_id=1, db=mock_db)
            assert exc_info.value.status_code == 500
            assert exc_info.value.detail == "Failed to get agent status"

def test_get_metrics_success(mock_db):
    metrics = {"cpu": 45.5, "memory": 1024}
    with patch("backend.app.api.routes.agents.get_metrics_for_agent", return_value=metrics):
        response = router.get("/{agent_id}/metrics")(lambda agent_id, db: {})(agent_id=1, db=mock_db)
        assert response == metrics

def test_get_metrics_exception_handling(mock_db):
    with patch("backend.app.api.routes.agents.get_metrics_for_agent", side_effect=Exception("Metrics error")):
        with pytest.raises(HTTPException) as exc_info:
            router.get("/{agent_id}/metrics")(lambda agent_id, db: {})(agent_id=1, db=mock_db)
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Failed to retrieve agent metrics"