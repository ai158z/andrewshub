import pytest
from unittest.mock import AsyncMock, Mock, patch
from fastapi import HTTPException
from backend.src.api.calculator import calculate_staking_rewards, get_calculator_config
from backend.src.models.staking import NetworkStats

@pytest.fixture
def valid_request():
    return {
        "stake": 1000.0,
        "duration": 30,
        "network": "ethereum",
        "compound": True
    }

@pytest.fixture
def invalid_request():
    return {
        "stake": -100.0,
        "duration": 0,
        "network": "invalid_network",
        "compound": "not_boolean"
    }

@pytest.fixture
def network_stats():
    return NetworkStats(
        network_name="ethereum",
        apr=0.05,
        token_symbol="ETH",
        total_staked=32000000,
        validator_count=500000
    )

def test_get_calculator_config():
    config = get_calculator_config()
    assert "min_stake" in config
    assert "max_stake" in config
    assert "min_duration" in config
    assert "max_duration" in config
    assert "supported_networks" in config

@pytest.mark.asyncio
async def test_calculate_staking_rewards_success(valid_request, network_stats):
    with patch('backend.src.services.chain_api.ChainAPIClient') as mock_chain, \
         patch('backend.src.services.price_oracle.PriceOracle') as mock_oracle:
        
        # Setup mocks
        mock_chain_instance = Mock()
        mock_chain_instance.fetch_network_stats = AsyncMock(return_value=network_stats)
        mock_chain.return_value = mock_chain_instance
        
        mock_oracle_instance = Mock()
        mock_oracle_instance.get_current_price = Mock(return_value=2000.0)
        mock_oracle.return_value = mock_oracle_instance
        
        # Mock utility functions
        with patch('backend.src.utils.calculations.calculate_rewards') as mock_calc, \
             patch('backend.test_calculator.project_rewards') as mock_project:
            
            mock_calc.return_value = 1.0  # daily rewards
            mock_project.return_value = {"30_days": 30.0}
            
            result = await calculate_staking_rewards(valid_request)
            
            assert result.daily_rewards == 1.0
            assert result.total_rewards == 1.0
            assert result.usd_value == 2000.0
            assert "30_days" in result.projected_rewards

@pytest.mark.asyncio
async def test_calculate_staking_rewards_invalid_input(invalid_request):
    with pytest.raises(HTTPException) as exc_info:
        await calculate_staking_rewards(invalid_request)
    assert exc_info.value.status_code == 400

@pytest.mark.asyncio
async def test_calculate_staking_rewards_network_stats_failure(valid_request):
    with patch('backend.src.services.chain_api.ChainAPIClient') as mock_chain:
        mock_chain_instance = Mock()
        mock_chain_instance.fetch_network_stats = AsyncMock(return_value=None)
        mock_chain.return_value = mock_chain_instance
        
        with pytest.raises(HTTPException) as exc_info:
            await calculate_staking_rewards(valid_request)
        assert exc_info.value.status_code == 400
        assert "Failed to fetch network statistics" in exc_info.value.detail

@pytest.mark.asyncio
async def test_calculate_staking_rewards_calculation_error(valid_request, network_stats):
    with patch('backend.src.services.chain_api.ChainAPIClient') as mock_chain, \
         patch('backend.src.services.price_oracle.PriceOracle') as mock_oracle, \
         patch('backend.src.utils.calculations.calculate_rewards') as mock_calc:
        
        mock_chain_instance = Mock()
        mock_chain_instance.fetch_network_stats = AsyncMock(return_value=network_stats)
        mock_chain.return_value = mock_chain_instance
        
        mock_oracle_instance = Mock()
        mock_oracle_instance.get_current_price = Mock(return_value=2000.0)
        mock_oracle.return_value = mock_oracle_instance
        
        mock_calc.side_effect = Exception("Calculation error")
        
        with pytest.raises(HTTPException) as exc_info:
            await calculate_staking_rewards(valid_request)
        assert exc_info.value.status_code == 500

@pytest.mark.asyncio
async def test_calculate_staking_rewards_validation_failure(valid_request):
    with patch('backend.src.utils.validators.validate_staking_input') as mock_validate:
        mock_validate.return_value = False
        
        with pytest.raises(HTTPException) as exc_info:
            await calculate_staking_rewards(valid_request)
        assert exc_info.value.status_code == 400

@pytest.mark.asyncio
async def test_calculate_staking_rewards_duration_validation_failure(valid_request):
    with patch('backend.src.utils.validators.validate_duration') as mock_validate_duration:
        mock_validate_duration.return_value = False
        
        with pytest.raises(HTTPException) as exc_info:
            await calculate_staking_rewards(valid_request)
        assert exc_info.value.status_code == 400

@pytest.mark.asyncio
async def test_calculate_staking_rewards_negative_stake():
    request = {
        "stake": -100.0,
        "duration": 30,
        "network": "ethereum"
    }
    
    with pytest.raises(HTTPException) as exc_info:
        await calculate_staking_rewards(request)
    assert exc_info.value.status_code == 400

@pytest.mark.asyncio
async def test_calculate_staking_rewards_zero_duration():
    request = {
        "stake": 1000.0,
        "duration": 0,
        "network": "ethereum"
    }
    
    with pytest.raises(HTTPException) as exc_info:
        await calculate_staking_rewards(request)
    assert exc_info.value.status_code == 400

@pytest.mark.asyncio
async def test_calculate_staking_rewards_large_stake():
    request = {
        "stake": 1000001.0,
        "duration": 30,
        "network": "ethereum"
    }
    
    with pytest.raises(HTTPException) as exc_info:
        await calculate_staking_rewards(request)
    assert exc_info.value.status_code == 400

@pytest.mark.asyncio
async def test_calculate_staking_rewards_invalid_network(valid_request):
    with patch('backend.src.services.chain_api.ChainAPIClient') as mock_chain:
        mock_chain_instance = Mock()
        mock_chain_instance.fetch_network_stats = AsyncMock(return_value=None)
        mock_chain.return_value = mock_chain_instance
        
        with pytest.raises(HTTPException) as exc_info:
            await calculate_staking_rewards(valid_request)
        assert exc_info.value.status_code == 400

@pytest.mark.asyncio
async def test_calculate_staking_rewards_price_oracle_failure(valid_request, network_stats):
    with patch('backend.src.services.chain_api.ChainAPIClient') as mock_chain, \
         patch('backend.src.services.price_oracle.PriceOracle') as mock_oracle:
        
        mock_chain_instance = Mock()
        mock_chain_instance.fetch_network_stats = AsyncMock(return_value=network_stats)
        mock_chain.return_value = mock_chain_instance
        
        mock_oracle_instance = Mock()
        mock_oracle_instance.get_current_price = Mock(return_value=None)
        mock_oracle.return_value = mock_oracle_instance
        
        result = await calculate_staking_rewards(valid_request)
        assert result.usd_value == 0.0

@pytest.mark.asyncio
async def test_calculate_staking_rewards_compound_false(valid_request, network_stats):
    valid_request["compound"] = False
    
    with patch('backend.src.services.chain_api.ChainAPIClient') as mock_chain, \
         patch('backend.src.services.price_oracle.PriceOracle') as mock_oracle:
        
        mock_chain_instance = Mock()
        mock_chain_instance.fetch_network_stats = AsyncMock(return_value=network_stats)
        mock_chain.return_value = mock_chain_instance
        
        mock_oracle_instance = Mock()
        mock_oracle_instance.get_current_price = Mock(return_value=2000.0)
        mock_oracle.return_value = mock_oracle_instance
        
        with patch('backend.src.utils.calculations.calculate_rewards') as mock_calc, \
             patch('backend.src.utils.calculations.project_rewards') as mock_project:
            
            mock_calc.return_value = 2.0
            mock_project.return_value = {"projection": "data"}
            
            result = await calculate_staking_rewards(valid_request)
            assert result.daily_rewards == 2.0

@pytest.mark.asyncio
async def test_calculate_staking_rewards_no_compound(valid_request, network_stats):
    valid_request["compound"] = False
    
    with patch('backend.src.services.chain_api.ChainAPIClient') as mock_chain, \
         patch('backend.src.services.price_oracle.PriceOracle') as mock_oracle:
        
        mock_chain_instance = Mock()
        mock_chain_instance.fetch_network_stats = AsyncMock(return_value=network_stats)
        mock_chain.return_value = mock_chain_instance
        
        mock_oracle_instance = Mock()
        mock_oracle_instance.get_current_price = Mock(return_value=2000.0)
        mock_oracle.return_value = mock_oracle_instance
        
        with patch('backend.src.utils.calculations.calculate_rewards') as mock_calc, \
             patch('backend.src.utils.calculations.project_rewards') as mock_project:
            
            mock_calc.return_value = 5.0
            mock_project.return_value = {"projection": "data"}
            
            result = await calculate_staking_rewards(valid_request)
            assert result.total_rewards == 5.0

@pytest.mark.asyncio
async def test_calculate_staking_rewards_exception_handling(valid_request):
    with pytest.raises(HTTPException) as exc_info:
        with patch('backend.src.services.chain_api.ChainAPIClient') as mock_chain:
            mock_chain_instance = Mock()
            mock_chain_instance.fetch_network_stats = AsyncMock(side_effect=Exception("API Error"))
            mock_chain.return_value = mock_chain_instance
            
            await calculate_staking_rewards(valid_request)
    
    assert exc_info.value.status_code == 500
    assert "Error calculating staking rewards" in exc_info.value.detail

@pytest.mark.asyncio
async def test_calculate_staking_rewards_large_duration(valid_request, network_stats):
    valid_request["duration"] = 400  # Above max duration
    
    with pytest.raises(HTTPException) as exc_info:
        await calculate_staking_rewards(valid_request)
    # Should be caught by input validation

@pytest.mark.asyncio
async def test_calculate_staking_rewards_small_stake(valid_request, network_stats):
    valid_request["stake"] = 0.5  # Below minimum
    
    with pytest.raises(HTTPException) as exc_info:
        await calculate_staking_rewards(valid_request)
    # Should be caught by input validation

@pytest.mark.asyncio
async def test_calculate_staking_rewards_valid_boundaries(valid_request, network_stats):
    # Test with exact boundary values
    valid_request["stake"] = 1.0  # min value
    valid_request["duration"] = 1   # min duration
    
    with patch('backend.src.services.chain_api.ChainAPIClient') as mock_chain, \
         patch('backend.src.services.price_oracle.PriceOracle') as mock_oracle:
        
        mock_chain_instance = Mock()
        mock_chain_instance.fetch_network_stats = AsyncMock(return_value=network_stats)
        mock_chain.return_value = mock_chain_instance
        
        mock_oracle_instance = Mock()
        mock_oracle_instance.get_current_price = Mock(return_value=2000.0)
        mock_oracle.return_value = mock_oracle_instance
        
        with patch('backend.src.utils.calculations.calculate_rewards') as mock_calc:
            mock_calc.return_value = 1.0
            result = await calculate_staking_rewards(valid_request)
            assert result is not None

@pytest.mark.asyncio
async def test_calculate_staking_rewards_projected_rewards(valid_request, network_stats):
    with patch('backend.src.services.chain_api.ChainAPIClient') as mock_chain, \
         patch('backend.src.services.price_oracle.PriceOracle') as mock_oracle:
        
        mock_chain_instance = Mock()
        mock_chain_instance.fetch_network_stats = AsyncMock(return_value=network_stats)
        mock_chain.return_value = mock_chain_instance
        
        mock_oracle_instance = Mock()
        mock_oracle_instance.get_current_price = Mock(return_value=2000.0)
        mock_oracle.return_value = mock_oracle_instance
        
        with patch('backend.src.utils.calculations.calculate_rewards') as mock_calc, \
             patch('backend.src.utils.calculations.project_rewards') as mock_project:
            
            mock_calc.return_value = 2.5
            mock_project.return_value = {"30_days": 75.0, "60_days": 150.0}
            
            result = await calculate_staking_rewards(valid_request)
            assert "30_days" in result.projected_rewards
            assert "60_days" in result.projected_rewards

@pytest.mark.asyncio
async def test_calculate_staking_rewards_unsupported_network():
    request = {
        "stake": 1000.0,
        "duration": 30,
        "network": "unsupported_network"
    }
    
    with patch('backend.src.services.chain_api.ChainAPIClient') as mock_chain:
        mock_chain_instance = Mock()
        mock_chain_instance.fetch_network_stats = AsyncMock(return_value=None)
        mock_chain.return_value = mock_chain_instance
        
        with pytest.raises(HTTPException) as exc_info:
            await calculate_staking_rewards(request)
        assert exc_info.value.status_code == 400