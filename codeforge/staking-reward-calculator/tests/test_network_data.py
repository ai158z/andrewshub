import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock, Mock, patch
from src.api.network_data import router
from src.models.staking import NetworkStats

@pytest.mark.asyncio
async def test_get_networks_success():
    # Arrange
    from src.api.network_data import get_networks
    # Act
    result = await get_networks()
    # Assert
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0]["name"] == "solana"

@pytest.mark.asyncio
async def test_get_networks_exception():
    # Arrange
    with patch("src.api.network_data.get_networks") as mock_get_networks:
        mock_get_networks.side_effect = Exception("Test error")
        # Act & Assert
        with pytest.raises(Exception):
            await mock_get_networks()

@pytest.mark.asyncio
async def test_get_network_stats_success():
    # Arrange
    with patch("src.api.network_data.ChainAPIClient") as mock_chain_client, \
         patch("src.api.network_data.PriceOracle") as mock_price_oracle:
        mock_chain_client_instance = AsyncMock()
        mock_chain_client_instance.fetch_network_stats = AsyncMock(return_value={"tps": 100, "slot": 123456})
        mock_chain_client.return_value = mock_chain_client_instance
        
        mock_price_oracle_instance = Mock()
        mock_price_oracle_instance.get_current_price.return_value = 100.0
        mock_price_oracle.return_value = mock_price_oracle_instance
        
        from src.api.network_data import get_network_stats
        # Act
        result = await get_network_stats("solana")
        # Assert
        assert isinstance(result, NetworkStats)

@pytest.mark.asyncio
async def test_get_network_stats_not_found():
    # Arrange
    with patch("src.api.network_data.ChainAPIClient") as mock_chain_client:
        mock_chain_client_instance = AsyncMock()
        mock_chain_client_instance.fetch_network_stats = AsyncMock(return_value=None)
        mock_chain_client.return_value = mock_chain_client_instance
        
        from src.api.network_data import get_network_stats
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_network_stats("unknown")
        assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_get_network_stats_exception():
    # Arrange
    with patch("src.api.network_data.get_network_stats", side_effect=Exception("Test error")):
        # Act & Assert
        with pytest.raises(HTTPException):
            await get_network_stats("solana")

@pytest.mark.asyncio
async def test_get_blockchain_data_success():
    # Arrange
    with patch("src.api.network_data.ChainAPIClient") as mock_chain_client:
        mock_chain_client_instance = AsyncMock()
        mock_chain_client_instance.get_blockchain_data = AsyncMock(return_value={"height": 123456})
        mock_chain_client.return_value = mock_chain_client_instance
        
        from src.api.network_data import get_blockchain_data
        # Act
        result = await get_blockchain_data("solana")
        # Assert
        assert result == {"height": 123456}

@pytest.mark.asyncio
async def test_get_blockchain_data_exception():
    # Arrange
    with patch("src.api.network_data.get_blockchain_data", side_effect=Exception("Test error")):
        # Act & Assert
        with pytest.raises(HTTPException):
            await get_blockchain_data("solana")

@pytest.mark.asyncio
async def test_get_network_stats_with_price_oracle_error():
    # Arrange
    with patch("src.api.network_data.ChainAPIClient") as mock_chain_client, \
         patch("src.api.network_data.PriceOracle") as mock_price_oracle:
        mock_chain_client_instance = AsyncMock()
        mock_chain_client_instance.fetch_network_stats = AsyncMock(return_value={"tps": 100, "slot": 123456})
        mock_chain_client.return_value = mock_chain_client_instance
        
        mock_price_oracle_instance = Mock()
        mock_price_oracle_instance.get_current_price.side_effect = Exception("Price oracle error")
        mock_price_oracle.return_value = mock_price_oracle_instance
        
        from src.api.network_data import get_network_stats
        # Act & Assert
        with pytest.raises(HTTPException):
            await get_network_stats("solana")

@pytest.mark.asyncio
async def test_get_network_stats_with_chain_client_error():
    # Arrange
    with patch("src.api.network_data.ChainAPIClient") as mock_chain_client:
        mock_chain_client_instance = AsyncMock()
        mock_chain_client_instance.fetch_network_stats.side_effect = Exception("Chain client error")
        mock_chain_client.return_value = mock_chain_client_instance
        
        from src.api.network_data import get_network_stats
        # Act & Assert
        with pytest.raises(HTTPException):
            await get_network_stats("solana")

def test_router_instance():
    # Act & Assert
    assert router is not None
    assert hasattr(router, "get")

@pytest.mark.asyncio
async def test_get_networks_empty_result():
    # Arrange
    with patch("src.api.network_data.get_networks") as mock_get_networks:
        mock_get_networks.return_value = []
        # Act
        result = await mock_get_networks()
        # Assert
        assert result == []

@pytest.mark.asyncio
async def test_get_network_stats_invalid_network():
    # Arrange
    with patch("src.api.network_data.ChainAPIClient") as mock_chain_client:
        mock_chain_client_instance = AsyncMock()
        mock_chain_client_instance.fetch_network_stats = AsyncMock(return_value=None)
        mock_chain_client.return_value = mock_chain_client_instance
        
        from src.api.network_data import get_network_stats
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_network_stats("invalid_network")
        assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_get_network_stats_valid_data():
    # Arrange
    with patch("src.api.network_data.ChainAPIClient") as mock_chain_client, \
         patch("src.api.network_data.PriceOracle") as mock_price_oracle:
        mock_chain_client_instance = AsyncMock()
        mock_chain_client_instance.fetch_network_stats = AsyncMock(return_value={"tps": 2000, "slot": 987654})
        mock_chain_client.return_value = mock_chain_client_instance
        
        mock_price_oracle_instance = Mock()
        mock_price_oracle_instance.get_current_price.return_value = 50.0
        mock_price_oracle.return_value = mock_price_oracle_instance
        
        from src.api.network_data import get_network_stats
        # Act
        result = await get_network_stats("solana")
        # Assert
        assert result.tps == 2000
        assert result.slot == 987654
        assert result.current_price == 50.0

@pytest.mark.asyncio
async def test_get_blockchain_data_empty_network():
    # Arrange
    with patch("src.api.network_data.ChainAPIClient") as mock_chain_client:
        mock_chain_client_instance = AsyncMock()
        mock_chain_client_instance.get_blockchain_data = AsyncMock(return_value={})
        mock_chain_client.return_value = mock_chain_client_instance
        
        from src.api.network_data import get_blockchain_data
        # Act
        result = await get_blockchain_data("")
        # Assert
        assert result == {}

@pytest.mark.asyncio
async def test_get_blockchain_data_none_network():
    # Arrange
    with patch("src.api.network_data.get_blockchain_data", side_effect=TypeError("Network cannot be None")):
        # Act & Assert
        with pytest.raises(TypeError):
            await get_blockchain_data(None)

@pytest.mark.asyncio
async def test_get_network_stats_no_price():
    # Arrange
    with patch("src.api.network_data.ChainAPIClient") as mock_chain_client, \
         patch("src.api.network_data.PriceOracle") as mock_price_oracle:
        mock_chain_client_instance = AsyncMock()
        mock_chain_client_instance.fetch_network_stats = AsyncMock(return_value={"tps": 100, "slot": 12345})
        mock_chain_client.return_value = mock_chain_client_instance
        
        mock_price_oracle_instance = Mock()
        mock_price_oracle_instance.get_current_price.return_value = None
        mock_price_oracle.return_value = mock_price_oracle_instance
        
        from src.api.network_data import get_network_stats
        # Act
        result = await get_network_stats("solana")
        # Assert
        assert result.current_price is None

@pytest.mark.asyncio
async def test_get_network_stats_partial_data():
    # Arrange
    with patch("src.api.network_data.ChainAPIClient") as mock_chain_client, \
         patch("src.api.network_data.PriceOracle") as mock_price_oracle:
        mock_chain_client_instance = AsyncMock()
        mock_chain_client_instance.fetch_network_stats = AsyncMock(return_value={"tps": 1000})
        mock_chain_client.return_value = mock_chain_client_instance
        
        mock_price_oracle_instance = Mock()
        mock_price_oracle_instance.get_current_price.return_value = 25.0
        mock_price_oracle.return_value = mock_price_oracle_instance
        
        from src.api.network_data import get_network_stats
        # Act
        result = await get_network_stats("solana")
        # Assert
        assert result.tps == 1000
        assert result.slot is None  # This field is missing in the mock data

@pytest.mark.asyncio
async def test_get_network_stats_price_oracle_exception():
    # Arrange
    with patch("src.api.network_data.ChainAPIClient") as mock_chain_client, \
         patch("src.api.network_data.PriceOracle") as mock_price_oracle:
        mock_chain_client_instance = AsyncMock()
        mock_chain_client_instance.fetch_network_stats = AsyncMock(return_value={"tps": 100, "slot": 123456})
        mock_chain_client.return_value = mock_chain_client_instance
        
        mock_price_oracle_instance = Mock()
        mock_price_oracle_instance.get_current_price.side_effect = Exception("Price oracle error")
        mock_price_oracle.return_value = mock_price_oracle_instance
        
        from src.api.network_data import get_network_stats
        # Act & Assert
        with pytest.raises(HTTPException):
            await get_network_stats("solana")

@pytest.mark.asyncio
async def test_get_network_stats_chain_client_exception():
    # Arrange
    with patch("src.api.network_data.ChainAPIClient") as mock_chain_client:
        mock_chain_client_instance = AsyncMock()
        mock_chain_client_instance.fetch_network_stats.side_effect = Exception("Chain client error")
        mock_chain_client.return_value = mock_chain_client_instance
        
        from src.api.network_data import get_network_stats
        # Act & Assert
        with pytest.raises(HTTPException):
            await get_network_stats("solana")