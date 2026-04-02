import pytest
from src.validators import validate_stake_amount, validate_duration, validate_inputs

def test_validate_stake_amount_valid():
    assert validate_stake_amount(1000.0) == True
    assert validate_stake_amount(1.0) == True
    assert validate_stake_amount(0.1) == True

def test_validate_stake_amount_invalid():
    assert validate_stake_amount(-100.0) == False
    assert validate_stake_amount(0.0) == False

def test_validate_stake_amount_boundary():
    assert validate_stake_amount(0.09) == False  # Below minimum
    assert validate_stake_amount(0.1) == True   # Minimum valid

def test_validate_duration_valid():
    assert validate_duration(30) == True
    assert validate_duration(1) == True

def test_validate_duration_invalid():
    assert validate_duration(0) == False
    assert validate_duration(-5) == False

def test_validate_duration_boundary():
    assert validate_duration(1) == True   # Minimum valid
    assert validate_duration(0) == False  # Invalid

def test_validate_inputs_valid():
    assert validate_inputs(1000.0, 30, 0) == True

def test_validate_inputs_invalid_stake():
    assert validate_inputs(-1000.0, 30, 0) == False
    assert validate_inputs(0.0, 30, 0) == False

def test_validate_inputs_invalid_duration():
    assert validate_inputs(1000.0, 0, 0) == False
    assert validate_inputs(1000.0, -5, 0) == False

def test_validate_inputs_all_valid():
    assert validate_inputs(100.0, 30, 0) == True

def test_validate_inputs_edge_cases():
    assert validate_inputs(0.1, 1, 0) == True  # Minimum valid values
    assert validate_inputs(1.0, 1, 0) == True

def test_validate_inputs_invalid_edge_cases():
    assert validate_inputs(0.09, 30, 0) == False  # Below minimum stake
    assert validate_inputs(1000.0, 0, 0) == False   # Invalid duration
    assert validate_inputs(1000.0, 30, -1) == False  # Invalid fee

def test_validate_stake_amount_type_error():
    with pytest.raises(TypeError):
        validate_stake_amount("invalid")

def test_validate_duration_type_error():
    with pytest.raises(TypeError):
        validate_duration(30.5)  # Non-integer duration

def test_validate_inputs_type_error():
    with pytest.raises(TypeError):
        validate_inputs("invalid", 30, 0)

def test_validate_stake_amount_none():
    with pytest.raises(TypeError):
        validate_stake_amount(None)

def test_validate_duration_none():
    with pytest.raises(TypeError):
        validate_duration(None)

def test_validate_inputs_none():
    with pytest.raises(TypeError):
        validate_inputs(None, 30, 0)

def test_validate_inputs_fee_boundary():
    assert validate_inputs(1000.0, 30, 100) == True  # High fee
    assert validate_inputs(1000.0, 30, -1) == False     # Invalid negative fee