import pytest
from fastapi import HTTPException
from src.utils.validators import validate_staking_input, validate_duration, StakingInput

def test_validate_staking_input_valid_data():
    data = {"stake": 1000.0, "duration": 365, "apr": 0.05}
    assert validate_staking_input(data) is True

def test_validate_staking_input_missing_field():
    data = {"stake": 1000.0, "duration": 365}
    assert validate_staking_input(data) is False

def test_validate_staking_input_invalid_type():
    data = {"stake": "invalid", "duration": 365, "apr": 0.05}
    assert validate_staking_input(data) is False

def test_validate_staking_input_negative_numbers():
    data = {"stake": -1000.0, "duration": 365, "apr": 0.05}
    assert validate_staking_input(data) is True

def test_validate_staking_input_mixed_invalid_data():
    data = {"stake": 1000.0, "duration": "invalid", "apr": 0.05}
    assert validate_staking_input(data) is False

def test_validate_duration_valid_positive():
    assert validate_duration(30) is True

def test_validate_duration_zero_days():
    assert validate_duration(0) is True

def test_validate_duration_negative_days():
    assert validate_duration(-1) is False

def test_validate_duration_invalid_type():
    assert validate_duration("invalid") is False

def test_validate_duration_float_input():
    assert validate_duration(30.5) is False

def test_staking_input_model_valid():
    staking_input = StakingInput(stake=1000.0, duration=365, apr=0.05)
    assert staking_input.is_valid() is True

def test_staking_input_model_negative_stake():
    staking_input = StakingInput(stake=-1000.0, duration=365, apr=0.05)
    assert staking_input.is_valid() is False

def test_staking_input_model_zero_duration():
    staking_input = StakingInput(stake=1000.0, duration=0, apr=0.05)
    assert staking_input.is_valid() is False

def staking_input_model_zero_apr():
    staking_input = StakingInput(stake=1000.0, duration=365, apr=0.0)
    assert staking_input.is_valid() is False

def test_staking_input_model_all_zero():
    staking_input = StakingInput(stake=0.0, duration=0, apr=0.0)
    assert staking_input.is_valid() is False

def test_staking_input_model_all_negative():
    staking_input = StakingInput(stake=-1000.0, duration=-365, apr=-0.05)
    assert staking_input.is_valid() is False

def test_validate_staking_input_empty_dict():
    data = {}
    assert validate_staking_input(data) is False

def test_validate_staking_input_none_value():
    data = {"stake": None, "duration": 365, "apr": 0.05}
    assert validate_staking_input(data) is False

def test_staking_input_model_large_numbers():
    staking_input = StakingInput(stake=1e10, duration=100000, apr=1000.0)
    assert staking_input.is_valid() is True