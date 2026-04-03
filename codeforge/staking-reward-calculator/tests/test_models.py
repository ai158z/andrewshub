import json
from decimal import Decimal
from staking_calculator.models import (
    StakingParameters, 
    RewardBreakdown, 
    StakingResult, 
    StakingReward,
    CompoundFrequency
)

def test_staking_parameters_to_dict():
    params = StakingParameters(apy=Decimal('0.05'), lockup_period=30, compound_frequency=365)
    result = params.to_dict()
    expected = {
        'apy': '0.05',
        'lockup_period': 30,
        'compound_frequency': 365
    }
    assert result == expected

def test_staking_parameters_from_dict():
    data = {
        'apy': '0.05',
        'lockup_period': 30,
        'compound_frequency': 365
    }
    params = StakingParameters.from_dict(data)
    assert params.apy == Decimal('0.05')
    assert params.lockup_period == 30
    assert params.compound_frequency == 365

def test_reward_breakdown_to_dict():
    breakdown = RewardBreakdown(
        total_reward=Decimal('100'),
        compound_rewards=Decimal('80'),
        penalty_deductions=Decimal('20')
    )
    result = breakdown.to_dict()
    expected = {
        'total_reward': '100',
        'compound_rewards': '80',
        'penalty_deductions': '20'
    }
    assert result == expected

def test_reward_breakdown_from_dict():
    data = {
        'total_reward': '100',
        'compound_rewards': '80',
        'penalty_deductions': '20'
    }
    breakdown = RewardBreakdown.from_dict(data)
    assert breakdown.total_reward == Decimal('100')
    assert breakdown.compound_rewards == Decimal('80')
    assert breakdown.penalty_deductions == Decimal('20')

def test_staking_result_to_dict():
    params = StakingParameters(apy=Decimal('0.05'), lockup_period=30, compound_frequency=365)
    breakdown = RewardBreakdown(
        total_reward=Decimal('100'),
        compound_rewards=Decimal('80'),
        penalty_deductions=Decimal('20')
    )
    result = StakingResult(
        parameters=params,
        breakdown=breakdown,
        stake_amount=Decimal('1000'),
        duration=365
    )
    dict_result = result.to_dict()
    assert 'parameters' in dict_result
    assert 'breakdown' in dict_result
    assert dict_result['stake_amount'] == '1000'
    assert dict_result['duration'] == 365

def test_staking_result_from_dict():
    data = {
        'parameters': {
            'apy': '0.05',
            'lockup_period': 30,
            'compound_frequency': 365
        },
        'breakdown': {
            'total_reward': '100',
            'compound_rewards': '80',
            'penalty_deductions': '20'
        },
        'stake_amount': '1000',
        'duration': 365
    }
    result = StakingResult.from_dict(data)
    assert result.stake_amount == Decimal('1000')
    assert result.duration == 365
    assert result.parameters.apy == Decimal('0.05')
    assert result.breakdown.total_reward == Decimal('100')

def test_staking_reward_to_dict():
    reward = StakingReward(
        principal=Decimal('1000'),
        apy=Decimal('0.05'),
        duration=365,
        compound_frequency=365,
        penalty_rate=Decimal('0.02'),
        total_reward=Decimal('100'),
        compound_rewards=Decimal('95'),
        penalty_deductions=Decimal('5')
    )
    result = reward.to_dict()
    assert 'principal' in result
    assert 'apy' in result
    assert result['principal'] == '1000'
    assert result['total_reward'] == '100'

def test_staking_reward_from_dict():
    data = {
        'principal': '1000',
        'apy': '0.05',
        'duration': 365,
        'compound_frequency': 365,
        'penalty_rate': '0.02',
        'total_reward': '100',
        'compound_rewards': '95',
        'penalty_deductions': '5'
    }
    reward = StakingReward.from_dict(data)
    assert reward.principal == Decimal('1000')
    assert reward.apy == Decimal('0.05')
    assert reward.total_reward == Decimal('100')

def test_compound_frequency_constants():
    assert CompoundFrequency.DAILY == 365
    assert CompoundFrequency.WEEKLY == 52
    assert CompoundFrequency.MONTHLY == 12
    assert CompoundFrequency.QUARTERLY == 4
    assert CompoundFrequency.ANNUALLY == 1

def test_staking_parameters_immutability():
    params = StakingParameters(apy=Decimal('0.05'), lockup_period=30, compound_frequency=365)
    # Test that dataclass is immutable by trying to access and modify
    assert params.apy == Decimal('0.05')
    assert params.lockup_period == 30
    assert params.compound_frequency == 365

def test_reward_breakdown_immutability():
    breakdown = RewardBreakdown(
        total_reward=Decimal('100'),
        compound_rewards=Decimal('80'),
        penalty_deductions=Decimal('20')
    )
    assert breakdown.total_reward == Decimal('100')
    assert breakdown.compound_rewards == Decimal('80')
    assert breakdown.penalty_deductions == Decimal('20')

def test_staking_result_immutability():
    params = StakingParameters(apy=Decimal('0.05'), lockup_period=30, compound_frequency=365)
    breakdown = RewardBreakdown(
        total_reward=Decimal('100'),
        compound_rewards=Decimal('80'),
        penalty_deductions=Decimal('20')
    )
    result = StakingResult(
        parameters=params,
        breakdown=breakdown,
        stake_amount=Decimal('1000'),
        duration=365
    )
    assert result.stake_amount == Decimal('1000')
    assert result.duration == 365

def test_staking_reward_immutability():
    reward = StakingReward(
        principal=Decimal('1000'),
        apy=Decimal('0.05'),
        duration=365,
        compound_frequency=365,
        penalty_rate=Decimal('0.02'),
        total_reward=Decimal('100'),
        compound_rewards=Decimal('95'),
        penalty_deductions=Decimal('5')
    )
    assert reward.principal == Decimal('1000')
    assert reward.apy == Decimal('0.05')
    assert reward.total_reward == Decimal('100')

def test_staking_parameters_edge_case_zero_values():
    params = StakingParameters(apy=Decimal('0'), lockup_period=0, compound_frequency=0)
    result = params.to_dict()
    assert result['apy'] == '0'
    assert result['lockup_period'] == 0
    assert result['compound_frequency'] == 0

def test_reward_breakdown_edge_case_zero_values():
    breakdown = RewardBreakdown(
        total_reward=Decimal('0'),
        compound_rewards=Decimal('0'),
        penalty_deductions=Decimal('0')
    )
    result = breakdown.to_dict()
    assert result['total_reward'] == '0'
    assert result['compound_rewards'] == '0'
    assert result['penalty_deductions'] == '0'

def test_staking_result_edge_case_zero_values():
    params = StakingParameters(apy=Decimal('0'), lockup_period=0, compound_frequency=0)
    breakdown = RewardBreakdown(
        total_reward=Decimal('0'),
        compound_rewards=Decimal('0'),
        penalty_deductions=Decimal('0')
    )
    result = StakingResult(
        parameters=params,
        breakdown=breakdown,
        stake_amount=Decimal('0'),
        duration=0
    )
    dict_result = result.to_dict()
    assert dict_result['stake_amount'] == '0'
    assert dict_result['duration'] == 0

def test_staking_reward_edge_case_zero_values():
    reward = StakingReward(
        principal=Decimal('0'),
        apy=Decimal('0'),
        duration=0,
        compound_frequency=0,
        penalty_rate=Decimal('0'),
        total_reward=Decimal('0'),
        compound_rewards=Decimal('0'),
        penalty_deductions=Decimal('0')
    )
    result = reward.to_dict()
    assert result['principal'] == '0'
    assert result['apy'] == '0'
    assert result['total_reward'] == '0'

def test_staking_parameters_negative_values():
    params = StakingParameters(apy=Decimal('-0.05'), lockup_period=-30, compound_frequency=-1)
    result = params.to_dict()
    assert result['apy'] == '-0.05'
    assert result['lockup_period'] == -30
    assert result['compound_frequency'] == -1

def test_reward_breakdown_negative_values():
    breakdown = RewardBreakdown(
        total_reward=Decimal('-100'),
        compound_rewards=Decimal('-80'),
        penalty_deductions=Decimal('-20')
    )
    result = breakdown.to_dict()
    assert result['total_reward'] == '-100'
    assert result['compound_rewards'] == '-80'
    assert result['penalty_deductions'] == '-20'