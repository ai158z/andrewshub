import pytest
from datetime import datetime
from src.models.staking import StakingCalculation, StakingResult, NetworkStats

def test_staking_calculation_valid():
    calc = StakingCalculation(
        stake_amount=1000.0,
        network="ethereum",
        duration_days=365,
        compound_frequency=365,
        include_price_change=True,
        price_change_percentage=5.0
    )
    assert calc.stake_amount == 1000.0
    assert calc.network == "ethereum"
    assert calc.duration_days == 365
    assert calc.compound_frequency == 365
    assert calc.include_price_change is True
    assert calc.price_change_percentage == 5.0

def test_staking_calculation_invalid_stake_amount():
    with pytest.raises(ValueError):
        StakingCalculation(
            stake_amount=0,
            network="ethereum",
            duration_days=365
        )

def test_staking_calculation_invalid_network():
    with pytest.raises(ValueError):
        StakingCalculation(
            stake_amount=1000.0,
            network="",
            duration_days=365
        )

def test_staking_calculation_invalid_duration():
    with pytest.raises(ValueError):
        StakingCalculation(
            stake_amount=1000.0,
            network="ethereum",
            duration_days=0
        )

def test_staking_calculation_negative_duration():
    with pytest.raises(ValueError):
        StakingCalculation(
            stake_amount=1000.0,
            network="ethereum",
            duration_days=-1
        )

def test_staking_calculation_too_long_duration():
    with pytest.raises(ValueError):
        StakingCalculation(
            stake_amount=1000.0,
            network="ethereum",
            duration_days=3651
        )

def test_staking_result_creation():
    result = StakingResult(
        total_rewards=100.0,
        total_value=1100.0,
        roi_percentage=10.0,
        apy=5.0,
        calculation_time=datetime.now()
    )
    assert result.total_rewards == 100.0
    assert result.total_value == 1100.0
    assert result.roi_percentage == 10.0
    assert result.apy == 5.0

def test_staking_result_with_projected_values():
    result = StakingResult(
        total_rewards=100.0,
        total_value=1100.0,
        roi_percentage=10.0,
        apy=5.0,
        projected_values={"year_1": 1100.0, "year_2": 1200.0}
    )
    assert result.projected_values is not None
    assert "year_1" in result.projected_values

def test_network_stats_creation():
    stat = NetworkStats(
        network_name="ethereum",
        total_staked=1000000.0,
        total_rewards=50000.0,
        average_apy=5.0,
        active_stakers=1000,
        total_validators=100
    )
    assert stat.network_name == "ethereum"
    assert stat.total_staked == 1000000.0
    assert stat.total_rewards == 50000.0
    assert stat.average_apy == 5.0

def test_network_stats_repr():
    stat = NetworkStats(
        network_name="ethereum",
        total_staked=1000000.0,
        total_rewards=50000.0
    )
    repr_str = repr(stat)
    assert "network_name='ethereum'" in repr_str
    assert "total_staked=1000000.0" in repr_str
    assert "total_rewards=50000.0" in repr_str

def test_staking_calculation_optional_fields_default():
    calc = StakingCalculation(
        stake_amount=1000.0,
        network="ethereum",
        duration_days=365
    )
    assert calc.compound_frequency == 365
    assert calc.include_price_change is False
    assert calc.price_change_percentage == 0.0

def test_staking_calculation_compound_frequency_validation():
    with pytest.raises(ValueError):
        StakingCalculation(
            stake_amount=1000.0,
            network="ethereum",
            duration_days=365,
            compound_frequency=0
        )

def test_staking_calculation_price_change_validation():
    calc = StakingCalculation(
        stake_amount=1000.0,
        network="ethereum",
        duration_days=365,
        include_price_change=True,
        price_change_percentage=100.0
    )
    assert calc.price_change_percentage == 100.0

def test_staking_calculation_price_change_over_limit():
    with pytest.raises(ValueError):
        StakingCalculation(
            stake_amount=1000.0,
            network="ethereum",
            duration_days=365,
            include_price_change=True,
            price_change_percentage=101.0
        )

def test_staking_calculation_price_change_under_limit():
    with pytest.raises(ValueError):
        StakingCalculation(
            stake_amount=1000.0,
            network="ethereum",
            duration_days=365,
            include_price_change=True,
            price_change_percentage=-101.0
        )

def test_staking_result_defaults():
    result = StakingResult(
        total_rewards=100.0,
        total_value=1100.0,
        roi_percentage=10.0,
        apy=5.0
    )
    assert result.projected_values is None
    assert result.calculation_time is None

def test_network_stats_attributes():
    stat = NetworkStats()
    assert hasattr(stat, 'id')
    assert hasattr(stat, 'network_name')
    assert hasattr(stat, 'total_staked')
    assert hasattr(stat, 'total_rewards')
    assert hasattr(stat, 'average_apy')
    assert hasattr(stat, 'active_stakers')
    assert hasattr(stat, 'total_validators')
    assert hasattr(stat, 'updated_at')

def test_staking_calculation_edge_case_min_values():
    calc = StakingCalculation(
        stake_amount=0.01,
        network="a",
        duration_days=1,
        compound_frequency=1
    )
    assert calc.stake_amount == 0.01
    assert calc.network == "a"
    assert calc.duration_days == 1
    assert calc.compound_frequency == 1

def test_staking_result_negative_values():
    result = StakingResult(
        total_rewards=-100.0,
        total_value=900.0,
        roi_percentage=-10.0,
        apy=-5.0
    )
    assert result.total_rewards == -100.0
    assert result.roi_percentage == -10.0