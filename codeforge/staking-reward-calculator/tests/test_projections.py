import pytest
from unittest.mock import AsyncMock, Mock, patch
from fastapi import HTTPException
from src.api.projections import calculate_projections, ProjectionRequest

@pytest.fixture
def valid_request():
    return ProjectionRequest(
        stake=1000.0,
        duration=365,
        network="ethereum",
        compound_frequency="daily"
    )

@pytest.fixture
def mock_network_stats():
    from src.models.staking import NetworkStats
    return NetworkStats(apy=0.12, currency="ETH")

@pytest.fixture
def mock_chain_client(mock_network_stats):
    with patch("src.api.projections.ChainAPIClient") as mock:
        instance = mock.return_value
        instance.fetch_network_stats = AsyncMock(return_value=mock_network_stats)
        yield instance

@pytest.fixture
def mock_price_oracle():
    with patch("src.api.projections.PriceOracle") as mock:
        instance = mock.return_value
        instance.get_current_price = Mock(return_value=2000.0)
        yield instance

def test_projection_request_valid_input(valid_request):
    assert valid_request.stake == 1000.0
    assert valid_request.duration == 365
    assert valid_request.network == "ethereum"

def test_projection_request_invalid_stake():
    with pytest.raises(ValueError):
        ProjectionRequest(stake=-100.0, duration=365, network="ethereum")

def test_projection_request_invalid_duration():
    with pytest.raises(ValueError):
        ProjectionRequest(stake=1000.0, duration=0, network="ethereum")

def test_calculate_projections_success(valid_request, mock_chain_client, mock_price_oracle):
    with patch("src.api.projections.project_rewards", return_value={
        "total_rewards": 120.0,
        "rewards_data": {}
    }):
        response = calculate_projections.__wrapped__(valid_request)
        assert response.total_rewards == 120.0
        assert response.currency == "ETH"

def test_calculate_projections_invalid_staking_input():
    request = ProjectionRequest(stake=-100.0, duration=365, network="ethereum")
    with pytest.raises(HTTPException) as exc_info:
        calculate_projections.__wrapped__(request)
    assert exc_info.value.status_code == 400

def test_calculate_projections_invalid_duration_input():
    request = ProjectionRequest(stake=1000.0, duration=-30, network="ethereum")
    with pytest.raises(HTTPException) as exc_info:
        calculate_projections.__wrapped__(request)
    assert exc_info.value.status_code == 400

def test_calculate_projections_network_stats_failure(mock_chain_client):
    mock_chain_client.fetch_network_stats = AsyncMock(return_value=None)
    with pytest.raises(HTTPException) as exc_info:
        calculate_projections.__wrapped__(valid_request)
    assert exc_info.value.status_code == 400

def test_calculate_projections_exception_handling(monkeypatch):
    def mock_validate_staking_input(data):
        raise Exception("Test exception")
    
    monkeypatch.setattr("src.api.projections.validate_staking_input", mock_validate_staking_input)
    with pytest.raises(HTTPException) as exc_info:
        calculate_projections.__wrapped__(valid_request)
    assert exc_info.value.status_code == 500

def test_calculate_projections_with_defaults():
    request = ProjectionRequest(stake=500.0, duration=180, network="polygon")
    with patch("src.api.projections.project_rewards", return_value={
        "total_rewards": 50.0,
        "rewards_data": {}
    }):
        response = calculate_projections.__wrapped__(request)
        assert response.total_rewards == 50.0

def test_calculate_projections_missing_network_stats(monkeypatch):
    monkeypatch.setattr("src.api.projections.ChainAPIClient", Mock())
    with patch("src.api.projections.ChainAPIClient") as mock_chain:
        mock_chain.return_value.fetch_network_stats = AsyncMock(return_value=None)
        with pytest.raises(HTTPException) as exc_info:
            calculate_projections.__wrapped__(valid_request)
        assert exc_info.value.status_code == 400

def test_calculate_projections_price_oracle_failure(monkeypatch):
    monkeypatch.setattr("src.api.projections.PriceOracle", Mock())
    with patch("src.api.projections.PriceOracle") as mock_oracle:
        mock_oracle.return_value.get_current_price = Mock(side_effect=Exception("Price oracle error"))
        with pytest.raises(Exception):
            calculate_projections.__wrapped__(valid_request)

def test_calculate_projections_compound_frequency_none():
    request = ProjectionRequest(
        stake=1000.0,
        duration=365,
        network="ethereum",
        compound_frequency=None
    )
    with patch("src.api.projections.project_rewards", return_value={
        "total_rewards": 120.0,
        "rewards_data": {}
    }):
        response = calculate_projections.__wrapped__(request)
        assert response.total_rewards == 120.0

def test_calculate_projections_compound_frequency_custom():
    request = ProjectionRequest(
        stake=1000.0,
        duration=365,
        network="ethereum",
        compound_frequency="monthly"
    )
    with patch("src.api.projections.project_rewards", return_value={
        "total_rewards": 100.0,
        "rewards_data": {}
    }):
        response = calculate_projections.__wrapped__(request)
        assert response.total_rewards == 100.0

def test_calculate_projections_small_values():
    request = ProjectionRequest(
        stake=0.001,
        duration=1,
        network="ethereum"
    )
    with patch("src.api.projections.project_rewards", return_value={
        "total_rewards": 0.0001,
        "rewards_data": {}
    }):
        response = calculate_projections.__wrapped__(request)
        assert response.total_rewards == 0.0001

def test_calculate_projections_large_stake():
    request = ProjectionRequest(
        stake=1000000.0,
        duration=3650,
        network="ethereum"
    )
    with patch("src.api.projections.project_rewards", return_value={
        "total_rewards": 120000.0,
        "rewards_data": {}
    }):
        response = calculate_projections.__wrapped__(request)
        assert response.total_rewards == 120000.0

def test_calculate_projections_zero_values():
    request = ProjectionRequest(
        stake=0.0,
        duration=0,
        network="ethereum"
    )
    with pytest.raises(HTTPException):
        calculate_projections.__wrapped__(request)

def test_calculate_projections_negative_stake():
    with pytest.raises(HTTPException) as exc_info:
        request = ProjectionRequest(
            stake=-500.0,
            duration=365,
            network="ethereum"
        )
        calculate_projections.__wrapped__(request)
    assert exc_info.value.status_code == 400

def test_calculate_projections_network_not_found():
    request = ProjectionRequest(
        stake=1000.0,
        duration=365,
        network="unknown_network"
    )
    with patch("src.api.projections.ChainAPIClient") as mock_chain:
        mock_chain.return_value.fetch_network_stats = AsyncMock(return_value=None)
        with pytest.raises(HTTPException) as exc_info:
            calculate_projections.__wrapped__(request)
        assert exc_info.value.status_code == 400

def test_calculate_projections_project_rewards_error():
    with patch("src.api.projections.project_rewards", side_effect=Exception("Calculation error")):
        with pytest.raises(HTTPException) as exc_info:
            calculate_projections.__wrapped__(valid_request)
        assert exc_info.value.status_code == 500