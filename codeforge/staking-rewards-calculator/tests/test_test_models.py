import pytest
from src.models import StakingResult, StakingConfig


def test_staking_result_creation_with_valid_values():
    result = StakingResult(
        gross_reward=1000.0,
        net_reward=950.0,
        penalty=50.0,
        duration=365
    )
    assert result.gross_reward == 1000.0
    assert result.net_reward == 950.0
    assert result.penalty == 50.0
    assert result.duration == 365


def test_staking_result_creation_with_zero_values():
    result = StakingResult(
        gross_reward=0.0,
        net_reward=0.0,
        penalty=0.0,
        duration=0
    )
    assert result.gross_reward == 0.0
    assert result.net_reward == 0.0
    assert result.penalty == 0.0
    assert result.duration == 0


def test_staking_result_creation_with_negative_values():
    result = StakingResult(
        gross_reward=-100.0,
        net_reward=-150.0,
        penalty=50.0,
        duration=-30
    )
    assert result.gross_reward == -100.0
    assert result.net_reward == -150.0
    assert result.penalty == 50.0
    assert result.duration == -30


def test_staking_config_creation_with_valid_values():
    config = StakingConfig(
        apy=5.5,
        compound_frequency=12,
        penalty_rate=0.02
    )
    assert config.apy == 5.5
    assert config.compound_frequency == 12
    assert config.penalty_rate == 0.02


def test_staking_config_creation_with_zero_values():
    config = StakingConfig(
        apy=0.0,
        compound_frequency=0,
        penalty_rate=0.0
    )
    assert config.apy == 0.0
    assert config.compound_frequency == 0
    assert config.penalty_rate == 0.0


def test_staking_config_creation_with_high_frequency():
    config = StakingConfig(
        apy=7.5,
        compound_frequency=365,
        penalty_rate=0.05
    )
    assert config.apy == 7.5
    assert config.compound_frequency == 365
    assert config.penalty_rate == 0.05


def test_staking_config_creation_with_extreme_values():
    config = StakingConfig(
        apy=100.0,
        compound_frequency=1000,
        penalty_rate=1.0
    )
    assert config.apy == 100.0
    assert config.compound_frequency == 1000
    assert config.penalty_rate == 1.0


def test_staking_config_creation_with_negative_apy():
    config = StakingConfig(
        apy=-5.0,
        compound_frequency=1,
        penalty_rate=0.1
    )
    assert config.apy == -5.0
    assert config.compound_frequency == 1
    assert config.penalty_rate == 0.1


def test_staking_result_type_consistency():
    result = StakingResult(1000.5, 950.3, 50.2, 365)
    assert isinstance(result.gross_reward, float)
    assert isinstance(result.net_reward, float)
    assert isinstance(result.penalty, float)
    assert isinstance(result.duration, int)


def test_staking_config_type_consistency():
    config = StakingConfig(5.5, 12, 0.02)
    assert isinstance(config.apy, float)
    assert isinstance(config.compound_frequency, int)
    assert isinstance(config.penalty_rate, float)


def test_staking_result_default_values():
    result = StakingResult(100.0, 90.0, 10.0, 30)
    assert result.gross_reward == 100.0
    assert result.net_reward == 90.0
    assert result.penalty == 10.0
    assert result.duration == 30


def test_staking_config_default_values():
    config = StakingConfig(7.5, 4, 0.03)
    assert config.apy == 7.5
    assert config.compound_frequency == 4
    assert config.penalty_rate == 0.03


def test_staking_result_large_values():
    result = StakingResult(
        gross_reward=1e9,
        net_reward=0.9e9,
        penalty=0.1e9,
        duration=1000000
    )
    assert result.gross_reward == 1e9
    assert result.net_reward == 0.9e9
    assert result.penalty == 0.1e9
    assert result.duration == 1000000


def test_staking_config_large_values():
    config = StakingConfig(
        apy=999.99,
        compound_frequency=999999,
        penalty_rate=0.99
    )
    assert config.apy == 999.99
    assert config.compound_frequency == 999999
    assert config.penalty_rate == 0.99


def test_staking_result_fractional_values():
    result = StakingResult(
        gross_reward=0.1,
        net_reward=0.09,
        penalty=0.01,
        duration=1
    )
    assert result.gross_reward == 0.1
    assert result.net_reward == 0.09
    assert result.penalty == 0.01
    assert result.duration == 1


def test_staking_config_fractional_values():
    config = StakingConfig(
        apy=0.01,
        compound_frequency=1,
        penalty_rate=0.001
    )
    assert config.apy == 0.01
    assert config.compound_frequency == 1
    assert config.penalty_rate == 0.001


def test_staking_result_attribute_access():
    result = StakingResult(100, 95, 5, 30)
    assert hasattr(result, 'gross_reward')
    assert hasattr(result, 'net_reward')
    assert hasattr(result, 'penalty')
    assert hasattr(result, 'duration')


def test_staking_config_attribute_access():
    config = StakingConfig(5.0, 12, 0.02)
    assert hasattr(config, 'apy')
    assert hasattr(config, 'compound_frequency')
    assert hasattr(config, 'penalty_rate')


def test_staking_result_equality():
    result1 = StakingResult(100.0, 95.0, 5.0, 30)
    result2 = StakingResult(100.0, 95.0, 5.0, 30)
    assert result1.gross_reward == result2.gross_reward
    assert result1.net_reward == result2.net_reward
    assert result1.penalty == result2.penalty
    assert result1.duration == result2.duration


def test_staking_config_equality():
    config1 = StakingConfig(5.5, 12, 0.02)
    config2 = StakingConfig(5.5, 12, 0.02)
    assert config1.apy == config2.apy
    assert config1.compound_frequency == config2.compound_frequency
    assert config1.penalty_rate == config2.penalty_rate