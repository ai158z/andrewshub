import pytest
import json
from src.app import create_app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_calculate_rewards_valid_input(client):
    """Test calculate rewards endpoint with valid input data."""
    response = client.post('/api/calculate', json={
        'principal': 1000,
        'apr': 0.05,
        'duration': 365
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_reward' in data
    assert 'final_amount' in data


def test_calculate_rewards_missing_principal(client):
    """Test calculate rewards endpoint with missing principal field."""
    response = client.post('/api/calculate', json={
        'apr': 0.05,
        'duration': 365
    })
    
    assert response.status_code == 400


def test_calculate_rewards_missing_apr(client):
    """Test calculate rewards endpoint with missing apr field."""
    response = client.post('/api/calculate', json={
        'principal': 1000,
        'duration': 365
    })
    
    assert response.status_code == 400


def test_calculate_rewards_missing_duration(client):
    """Test calculate rewards endpoint with missing duration field."""
    response = client.post('/api/calculate', json={
        'principal': 1000,
        'apr': 0.05
    })
    
    assert response.status_code == 400


def test_calculate_rewards_invalid_data_types(client):
    """Test calculate rewards endpoint with invalid data types."""
    response = client.post('/api/calculate', json={
        'principal': 'invalid',
        'apr': 'invalid',
        'duration': 'invalid'
    })
    
    assert response.status_code == 400


def test_calculate_rewards_zero_values(client):
    """Test calculate rewards with zero values."""
    response = client.post('/api/calculate', json={
        'principal': 0,
        'apr': 0,
        'duration': 0
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total_reward'] == 0
    assert data['final_amount'] == 0


def test_calculate_rewards_negative_principal(client):
    """Test calculate rewards with negative principal."""
    response = client.post('/api/calculate', json={
        'principal': -1000,
        'apr': 0.05,
        'duration': 365
    })
    
    assert response.status_code == 400


def test_homepage_returns_html(client):
    """Test homepage returns HTML content."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<html>' in response.data
    assert b'Staking Reward Calculator' in response.data


def test_api_endpoint_post_only(client):
    """Test that API endpoint only accepts POST requests."""
    response = client.get('/api/calculate')
    assert response.status_code == 405


def test_api_endpoint_returns_json_content_type(client):
    """Test that API endpoint returns correct content type."""
    response = client.post('/api/calculate', json={
        'principal': 1000,
        'apr': 0.05,
        'duration': 365
    })
    
    assert response.status_code == 200
    assert response.content_type == 'application/json'