import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from src.models import Skill, Task, Prediction, User

# Create a test client
@pytest.fixture
def client():
    from src.main import app
    return TestClient(app)

# Mock data
@pytest.fixture
def mock_skill():
    return Skill(
        id="skill_1",
        name="Python Programming",
        category="Programming",
        description="Learn Python from scratch"
    )

@pytest.fixture
def mock_task():
    return Task(
        id="task_1",
        name="Complete Python exercise",
        skill_id="skill_1",
        difficulty=5
    )

@pytest.fixture
def mock_user():
    return User(username="testuser", password="testpass")

@pytest.fixture
def mock_token():
    return "valid_token"

# Test health check endpoint
def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Skill Library Predictor API is running" in response.json()["message"]

# Test skill management endpoints
@patch("src.main.skill_library")
def test_add_skill(mock_skill_lib, client, mock_skill):
    mock_skill_lib.add_skill.return_value = mock_skill
    response = client.post("/skills/", json=mock_skill.dict(), headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert response.json()["name"] == "Python Programming"

@patch("src.main.skill_library")
def test_get_skills(mock_skill_lib, client):
    mock_skill_lib.get_skills.return_value = []
    response = client.get("/skills/", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200

@patch("src.main.skill_library")
def test_update_skill(mock_skill_lib, client, mock_skill):
    mock_skill_lib.update_skill.return_value = mock_skill
    response = client.put("/skills/skill_1", json=mock_skill.dict(), headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200

@patch("src.main.skill_library")
def test_remove_skill(mock_skill_lib, client):
    mock_skill_lib.remove_skill.return_value = True
    response = client.delete("/skills/skill_1", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert "removed successfully" in response.json()["message"]

# Test prediction endpoints
@patch("src.main.task_predictor")
def test_predict_task_outcome(mock_predictor, client, mock_task):
    mock_prediction = Prediction(task_id="task_1", probability=0.85, outcome=True)
    mock_predictor.predict_task_outcome.return_value = mock_prediction
    response = client.post("/predict/", json=mock_task.dict(), headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert "probability" in response.json()

# Test model update endpoint
@patch("src.main.task_predictor")
def test_update_model(mock_predictor, client):
    response = client.post("/model/update", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert "updated successfully" in response.json()["message"]

# Test curiosity budget endpoints
@patch("src.main.curiosity_budget")
def test_adjust_budget(mock_budget, client):
    response = client.post("/budget/adjust", json={"success_rate": 0.75}, headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200

@patch("src.main.curiosity_budget")
def test_get_budget(mock_budget, client):
    mock_budget.get_budget.return_value = 100
    response = client.get("/budget/", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert "budget" in response.json()

@patch("src.main.curiosity_budget")
def test_update_success_rate(mock_budget, client):
    response = client.post("/budget/success", 
                          json={"success_count": 8, "total_count": 10}, 
                          headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert "Success rate updated successfully" in response.json()["message"]

# Test proficiency endpoints
@patch("src.main.proficiency_tracker")
def test_update_proficiency(mock_proficiency, client):
    response = client.post("/proficiency/update", 
                         json={"skill_id": "skill_1", "proficiency_level": 0.75},
                         headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200

@patch("src.main.proficiency_tracker")
def test_get_proficiency_history(mock_proficiency, client):
    mock_proficiency.get_proficiency_history.return_value = [0.5, 0.6, 0.7]
    response = client.get("/proficiency/skill_1", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200

# Test outcome prediction endpoints
@patch("src.main.outcome_predictor")
def test_predict_outcome(mock_outcome, client, mock_task):
    mock_prediction = Prediction(task_id="task_1", probability=0.9, outcome=True)
    mock_outcome.predict_outcome.return_value = mock_prediction
    response = client.post("/outcome/predict", json=mock_task.dict(), headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200

@patch("src.main.outcome_predictor")
def test_train_model(mock_outcome, client):
    response = client.post("/outcome/train", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert "Model trained successfully" in response.json()["message"]

# Test authentication
@patch("src.main.auth_manager")
def test_login(mock_auth, client, mock_user):
    mock_auth.generate_token.return_value = "test_token"
    response = client.post("/auth/login", json=mock_user.dict())
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

# Test error cases
def test_predict_task_outcome_unauthorized(client, mock_task):
    response = client.post("/predict/", json=mock_task.dict())
    assert response.status_code == 401

def test_add_skill_unauthorized(client, mock_skill):
    response = client.post("/skills/", json=mock_skill.dict())
    assert response.status_code == 401

@patch("src.main.skill_library")
def test_remove_nonexistent_skill(mock_skill_lib, client):
    mock_skill_lib.remove_skill.return_value = False
    response = client.delete("/skills/nonexistent", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 404

# Test data validation
def test_root_endpoint_content(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Skill Library Predictor API is running"

# Test with invalid data
def test_predict_with_invalid_data(client):
    invalid_task = {"invalid": "data"}
    response = client.post("/predict/", json=invalid_task, headers={"Authorization": "Bearer valid_token"})
    # Should fail validation
    assert response.status_code == 422

def test_add_skill_invalid_data(client):
    invalid_data = {"invalid_field": "test"}
    response = client.post("/skills/", json=invalid_data, headers={"Authorization": "Bearer valid_token"})
    # Should fail validation
    assert response.status_code == 422