import pytest
from src.validators import validate_stake_amount, validate_duration, validate_inputs


def test_validate_stake_amount_valid():
    assert validate_stake_amount(1000.0) is True


def test_validate_stake_amount_too_low():
    assert validate_stake_amount(0.5) is False


def test_validate_stake_amount_too_high():
    assert validate_stake_amount(2000000.0) is False


def test_validate_stake_amount_invalid_type():
    assert validate_stake_amount("invalid") is False


def test_validate_stake_amount_zero():
    assert validate_stake_amount(0) is False


def test_validate_stake_amount_negative():
    assert validate_stake_amount(-50) is False


def test_validate_stake_amount_float_min_boundary():
    assert validate_stake_amount(1.0) is True


def test_validate_stake_amount_float_max_boundary():
    assert validate_stake_amount(1000000.0) is True


def test_validate_duration_valid():
    assert validate_duration(30) is True


def test_validate_duration_invalid_type():
    assert validate_duration("thirty") is False


def test_validate_duration_too_low():
    assert validate_duration(0) is False


def test_validate_duration_too_high():
    assert validate_duration(5000) is False


def test_validate_inputs_all_valid():
    assert validate_inputs(1000.0, 30, 10) is True


def test_validate_inputs_invalid_stake_amount():
    assert validate_inputs(0.5, 30, 10) is False


def test_validate_inputs_invalid_duration():
    assert validate_inputs(1000.0, 0, 10) is False


def test_validate_inputs_invalid_lockup_type():
    assert validate_inputs(1000.0, 30, "invalid") is False


def test_validate_inputs_lockup_exceeds_duration():
    assert validate_inputs(1000.0, 30, 50) is False


def test_validate_inputs_negative_lockup():
    assert validate_inputs(1000.0, 30, -5) is False


def test_validate_inputs_lockup_zero_default():
    assert validate_inputs(1000.0, 30) is True