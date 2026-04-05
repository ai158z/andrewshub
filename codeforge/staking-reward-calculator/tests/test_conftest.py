import os
import pytest
from unittest.mock import Mock
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate


def test_mock_redis_get_set():
    mock_redis = MockRedis()
    mock_redis.set("test_key", "test_value")
    assert mock_redis.get("test_key") == "test_value"
    assert mock_redis.get("nonexistent_key") is None


def test_mock_redis_flushall():
    mock_redis = MockRedis()
    mock_redis.set("key1", "value1")
    mock_redis.set("key2", "value2")
    mock_redis.flushall()
    assert len(mock_redis.data) == 0


def test_mock_stake_data_fixture(mock_stake_data):
    assert isinstance(mock_stake_data, StakeData)
    assert mock_stake_data.amount == 1000.0
    assert mock_stake_data.duration == 30
    assert mock_stake_data.validator_address == "0x1234567890123456789012345678901234567890"


def test_mock_reward_rate_fixture(mock_reward_rate):
    assert isinstance(mock_reward_rate, RewardRate)
    assert mock_reward_rate.annual_rate == 0.05
    assert mock_reward_rate.daily_rate == 0.000137
    assert mock_reward_rate.network == "ethereum"


def test_mock_stake_data_dict_fixture(mock_stake_data_dict):
    assert isinstance(mock_stake_data_dict, dict)
    assert mock_stake_data_dict["amount"] == 1000.0
    assert mock_stake_data_dict["duration"] == 30
    assert mock_stake_data_dict["validator_address"] == "0x1234567890123456789012345678901234567890"


def test_mock_reward_rate_dict_fixture(mock_reward_rate_dict):
    assert isinstance(mock_reward_rate_dict, dict)
    assert mock_reward_rate_dict["annual_rate"] == 0.05
    assert mock_reward_rate_dict["daily_rate"] == 0.000137
    assert mock_reward_rate_dict["network"] == "ethereum"


def test_mock_rewards_result_fixture(mock_rewards_result):
    assert isinstance(mock_rewards_result, dict)
    assert mock_rewards_result["total_rewards"] == 15.0
    assert mock_rewards_result["daily_rewards"] == 0.5
    assert mock_rewards_result["annual_rate"] == 0.05
    assert mock_rewards_result["projected_rewards"] == 182.5


def test_mock_blockchain_response_dict_fixture(mock_blockchain_response_dict):
    assert isinstance(mock_blockchain_response_dict, dict)
    assert "jsonrpc" in mock_blockchain_response_dict
    assert "result" in mock_blockchain_response_dict
    assert mock_blockchain_response_dict["result"]["reward_rate"] == "0.05"


def test_environment_setup():
    assert os.environ.get("BLOCKCHAIN_NODE_URL") == "https://mainnet.infura.io/v3/test"
    assert os.environ.get("API_ENDPOINT_URL") == "https://api.example.com"
    assert os.environ.get("REDIS_URL") == "redis://localhost:6379/0"


def test_environment_cleanup():
    # This test should run after setup_environment fixture
    # and check that environment is properly cleaned up
    assert os.environ.get("BLOCKCHAIN_NODE_URL") is None
    assert os.environ.get("API_ENDPOINT_URL") is None
    assert os.environ.get("REDIS_URL") is None


def test_mock_cache_fixture(mock_cache):
    assert isinstance(mock_cache, dict)
    assert len(mock_cache) == 0


def test_mock_redis_injection(mock_redis):
    assert isinstance(mock_redis, MockRedis)
    mock_redis.set("test", "value")
    assert mock_redis.get("test") == "value"


def test_fixture_types():
    # Test that fixtures return expected types
    stake_data = StakeData(
        validator_address="0x1234567890123456789012345678901234567890",
        amount=1000.0,
        duration=30
    )
    reward_rate = RewardRate(
        annual_rate=0.05,
        daily_rate=0.000137,
        network="ethereum"
    )
    assert isinstance(stake_data, StakeData)
    assert isinstance(reward_rate, RewardRate)