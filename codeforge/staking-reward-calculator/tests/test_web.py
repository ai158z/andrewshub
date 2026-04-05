from unittest.mock import patch, MagicMock
from src.routes.web import web
from decimal import Decimal
import pytest

@pytest.fixture
def client():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(web)
    return app.test_client()

def test_index_gets_main_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_index_handles_template_error(client, monkeypatch):
    mock_render = MagicMock(side_effect=Exception("template error"))
    monkeypatch.setattr("src.routes.web.render_template", mock_render)
    response = client.get('/')
    assert response.status_code == 500
    assert response.get_data(as_text=True) == "Error loading page"

def test_calculate_with_valid_data(client):
    response = client.post('/calculate', json={
        "principal": "1000",
        "apr": "5.5",
        "duration": 365
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "rewards" in data

def test_calculate_missing_data(client):
    response = client.post('/calculate', json=None)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_calculate_missing_fields(client):
    response = client.post('/calculate', json={"principal": "1000"})
    assert response.status_code == 400
    assert "Missing field" in response.get_json()["error"]

def test_calculate_invalid_numeric_values(client):
    response = client.post('/calculate', json={
        "principal": "invalid",
        "apr": "5.5",
        "duration": 365
    })
    assert response.status_code == 400
    assert "Invalid numeric values" in response.get_json()["error"]

def test_calculate_negative_principal(client):
    response = client.post('/calculate', json={
        "principal": "-1000",
        "apr": "5.5",
        "duration": 365
    })
    assert response.status_code == 400
    assert "Principal amount must be positive" in response.get_json()["error"]

def test_calculate_invalid_apr_range(client):
    response = client.post('/calculate', json={
        "principal": "1000",
        "apr": "150",
        "duration": 365
    })
    assert response.status_code == 400
    assert "APR must be between 0 and 100" in response.get_json()["error"]

def test_calculate_negative_duration(client):
    response = client.post('/calculate', json={
        "principal": "1000",
        "apr": "5.5",
        "duration": -100
    })
    assert response.status_code == 400
    assert "Duration must be non-negative" in response.get_json()["error"]

@patch('src.routes.web.calculate_rewards', return_value=Decimal("100.50"))
def test_calculate_returns_correct_structure(mock_calculate, client):
    response = client.post('/calculate', json={
        "principal": "1000",
        "apr": "5.5",
        "duration": 365
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "principal" in data
    assert "apr" in data
    assert "duration" in data
    assert "rewards" in data

def test_calculate_handles_internal_error(client, monkeypatch):
    mock_calc = MagicMock(side_effect=Exception("calculation error"))
    monkeypatch.setattr("src.routes.web.calculate_rewards", mock_calc)
    response = client.post('/calculate', json={
        "principal": "1000",
        "apr": "5.5",
        "duration": 365
    })
    assert response.status_code == 500
    assert "Calculation failed" in response.get_json()["error"]

def test_calculate_success_with_integer_inputs(client):
    response = client.post('/calculate', json={
        "principal": 1000,
        "apr": 5.5,
        "duration": 365
    })
    assert response.status_code == 200
    assert "rewards" in response.get_json()

def test_calculate_success_with_string_inputs(client):
    response = client.post('/calculate', json={
        "principal": "1000.50",
        "apr": "5.5",
        "duration": "365"
    })
    assert response.status_code == 200

def test_calculate_with_zero_values(client):
    response = client.post('/calculate', json={
        "principal": "0",
        "apr": "0",
        "duration": 0
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["rewards"] == 0.0

def test_calculate_with_max_apr(client):
    response = client.post('/calculate', json={
        "principal": "1000",
        "apr": "100",
        "duration": 365
    })
    assert response.status_code == 200

def test_calculate_with_min_apr(client):
    response = client.post('/calculate', json={
        "principal": "1000",
        "apr": "0",
        "duration": 365
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["rewards"] == 0.0

def test_calculate_with_large_duration(client):
    response = client.post('/calculate', json={
        "principal": "1000",
        "apr": "5",
        "duration": 10000
    })
    assert response.status_code == 200

def test_calculate_with_very_small_values(client):
    response = client.post('/calculate', json={
        "principal": "0.01",
        "apr": "0.01",
        "duration": 1
    })
    assert response.status_code == 200

def test_calculate_with_mismatched_types(client):
    response = client.post('/calculate', json={
        "principal": 1000.50,
        "apr": "5.5%",
        "duration": "365 days"
    })
    assert response.status_code == 400