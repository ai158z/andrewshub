import os
from typing import Any, Dict
import pytest
from unittest.mock import Mock
import redis
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate


class MockRedis:
    def __init__(self):
        self.data = {}

    def get(self, key: str) -> Any:
        return self.data.get(key, None)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value

    def flushall(self) -> None:
        self.data.clear()


@pytest.fixture
def mock_redis():
    return MockRedis()


@pytest.fixture
def mock_stake_data() -> StakeData:
    return StakeData(
        validator_address="0x1234567890123456789012345678901234567890",
        amount=1000.0,
        duration=30,
        network="ethereum"
    )


@pytest.fixture
def mock_reward_rate() -> RewardRate:
    return RewardRate(
        annual_rate=0.05,
        daily_rate=0.000137,
        network="ethereum",
        timestamp=1640995200
    )


@pytest.fixture
def mock_stake_data_dict():
    return {
        "validator_address": "0x1234567890123456789012345678901234567890",
        "amount": 1000.0,
        "duration": 30,
        "network": "ethereum"
    }


@pytest.fixture
def mock_reward_rate_dict():
    return {
        "annual_rate": 0.05,
        "daily_rate": 0.000137,
        "network": "ethereum",
        "timestamp": 1640995200
    }


@pytest.fixture
def mock_rewards_result():
    return {
        "total_rewards": 15.0,
        "daily_rewards": 0.5,
        "annual_rate": 0.05,
        "projected_rewards": 182.5
    }


def mock_blockchain_response() -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "reward_rate": "0.05",
            "block_number": 15000000,
            "timestamp": 1640995200
        }
    }


@pytest.fixture
def mock_blockchain_response_dict():
    return mock_blockchain_response()


@pytest.fixture
def mock_cache():
    return {}


@pytest.fixture(autouse=True)
def setup_environment():
    os.environ["BLOCKCHAIN_NODE_URL"] = "https://mainnet.infura.io/v3/test"
    os.environ["API_ENDPOINT_URL"] = "https://api.example.com"
    os.environ["REDIS_URL"] = "redis://localhost:6379/0"
    yield
    # Clean up environment variables
    for var in ["BLOCKCHAIN_NODE_URL", "API_ENDPOINT_URL", "REDIS_URL"]:
        if var in os.environ:
            del os.environ[var]


@pytest.fixture
def mock_redis():
    # Create a new instance of the MockRedis class for testing
    return MockRedis()