import pytest
from src.models import StakingResult, StakingConfig


def test_staking_result_initialization():
    result = StakingResult(gross_reward=100.0, net_reward=90.0, penalty=10.0, duration=365)
    assert result.gross_reward == 100.0
    assert result.net_reward == 90.0
    assert result.penalty == 10.0
    assert result.duration == 365


def test_staking_result_negative_gross_reward_raises_error():
    with pytest.raises(ValueError, match="Gross reward cannot be negative"):
        StakingResult(gross_reward=-10.0, net_reward=90.0, penalty=10.0, duration=365)


def test_staking_result_negative_net_reward_raises_error():
    with pytest.raises(ValueError, match="Net reward cannot be negative"):
        StakingResult(gross_reward=100.0, net_reward=-10.0, penalty=10.0, duration=365)


def test_staking_result_negative_penalty_raises_error():
    with pytest.raises(ValueError, match="Penalty cannot be negative"):
        StakingResult(gross_reward=100.0, net_reward=90.0, penalty=-10.0, duration=365)


def test_staking_result_negative_duration_raises_error():
    with pytest.raises(ValueError, match="Duration cannot be negative"):
        StakingResult(gross_reward=100.0, net_reward=90.0, penalty=10.0, duration=-365)


def test_staking_result_repr():
    result = StakingResult(gross_reward=100.0, net_reward=90.0, penalty=10.0, duration=365)
    expected = "StakingResult(gross_reward=100.0, net_reward=90.0, penalty=10.0, duration=365)"
    assert repr(result) == expected


def test_staking_result_equality():
    result1 = StakingResult(100.0, 90.0, 10.0, 365)
    result2 = StakingResult(100.0, 90.0, 10.0, 365)
    assert result1 == result2


def test_staking_result_inequality():
    result1 = StakingResult(100.0, 90.0, 10.0, 365)
    result2 = StakingResult(100.0, 85.0, 15.0, 365)
    assert result1 != result2


def test_staking_result_from_dict():
    data = {'gross_reward': 100.0, 'net_reward': 90.0, 'penalty': 10.0, 'duration': 365}
    result = StakingResult.from_dict(data)
    assert result.gross_reward == 100.0
    assert result.net_reward == 90.0
    assert result.penalty == 10.0
    assert result.duration == 365


def test_staking_config_initialization():
    config = StakingConfig(apy=0.05, compound_frequency=12, penalty_rate=0.01)
    assert config.apy == 0.05
    assert config.compound_frequency == 12
    assert config.penalty_rate == 0.01


def test_staking_config_invalid_apy_raises_error():
    with pytest.raises(ValueError, match="APY must be between 0 and 1"):
        StakingConfig(apy=1.5)


def test_staking_config_invalid_compound_frequency_raises_error():
    with pytest.raises(ValueError, match="Compound frequency must be positive"):
        StakingConfig(apy=0.05, compound_frequency=-1)


def test_staking_config_invalid_penalty_rate_raises_error():
    with pytest.raises(ValueError, match="Penalty rate must be between 0 and 1"):
        StakingConfig(apy=0.05, penalty_rate=1.5)


def test_staking_config_repr():
    config = StakingConfig(apy=0.05, compound_frequency=12, penalty_rate=0.01)
    expected = "StakingConfig(apy=0.05, compound_frequency=12, penalty_rate=0.01)"
    assert repr(config) == expected


def test_staking_config_equality():
    config1 = StakingConfig(apy=0.05, compound_frequency=12, penalty_rate=0.01)
    config2 = StakingConfig(apy=0.05, compound_frequency=12, penalty_rate=0.01)
    assert config1 == config2


def test_staking_config_inequality():
    config1 = StakingConfig(apy=0.05, compound_frequency=12, penalty_rate=0.01)
    config2 = StakingConfig(apy=0.03, compound_frequency=12, penalty_rate=0.01)
    assert config1 != config2


def test_staking_config_from_dict_with_defaults():
    data = {'apy': 0.05}
    config = StakingConfig.from_dict(data)
    assert config.apy == 0.05
    assert config.compound_frequency == 1
    assert config.penalty_rate == 0.0


def test_staking_config_from_dict_full():
    data = {'apy': 0.05, 'compound_frequency': 12, 'penalty_rate': 0.01}
    config = StakingConfig.from_dict(data)
    assert config.apy == 0.05
    assert config.compound_frequency == 12
    assert config.penalty_rate == 0.01


def test_staking_config_to_dict():
    config = StakingConfig(apy=0.05, compound_frequency=12, penalty_rate=0.01)
    data = config.to_dict()
    assert data == {'apy': 0.05, 'compound_frequency': 12, 'penalty_rate': 0.01}


def test_staking_config_default_values():
    config = StakingConfig(apy=0.05)
    assert config.apy == 0.05
    assert config.compound_frequency == 1
    assert config.penalty_rate == 0.0