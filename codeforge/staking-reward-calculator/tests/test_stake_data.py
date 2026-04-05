from datetime import datetime
from pydantic import ValidationError
import pytest
from src.models.stake_data import StakeData


def test_valid_stake_data():
    data = StakeData(
        amount=100.0,
        duration=30,
        network="ethereum",
        start_date=datetime.now()
    )
    assert data.amount == 100.0
    assert data.duration == 30
    assert data.network == "ethereum"


def test_stake_data_with_minimum_values():
    data = StakeData(
        amount=0.1,
        duration=1,
        network="a",
        start_date=None
    )
    assert data.amount == 0.1
    assert data.duration == 1
    assert data.network == "a"


def test_stake_data_without_start_date():
    data = StakeData(amount=1000.0, duration=90, network="polygon")
    assert data.start_date is None


def test_negative_amount_raises_validation_error():
    with pytest.raises(ValidationError):
        StakeData(amount=-50.0, duration=30, network="ethereum")


def test_zero_amount_raises_validation_error():
    with pytest.raises(ValidationError):
        StakeData(amount=0, duration=30, network="ethereum")


def test_negative_duration_raises_validation_error():
    with pytest.raises(ValidationError):
        StakeData(amount=100.0, duration=-5, network="ethereum")


def test_zero_duration_raises_validation_error():
    with pytest.raises(ValidationError):
        StakeData(amount=100.0, duration=0, network="ethereum")


def test_empty_network_raises_validation_error():
    with pytest.raises(ValidationError):
        StakeData(amount=100.0, duration=30, network="")


def test_whitespace_network_stripped():
    data = StakeData(
        amount=100.0,
        duration=30,
        network="  ethereum  "
    )
    assert data.network == "ethereum"


def test_network_validator_rejects_non_string():
    with pytest.raises(ValidationError):
        StakeData(amount=100.0, duration=30, network=123)


def test_network_validator_rejects_empty_string():
    with pytest.mark.xfail(raises=ValidationError):
        StakeData(amount=100.0, duration=30, network="")


def test_amount_validator_calls_external_validator(mocker):
    mocker.patch('src.validator.validate_stake_amount', return_value=False)
    with pytest.raises(ValidationError):
        StakeData(amount=100.0, duration=30, network="ethereum")


def test_valid_assignment_config_works():
    data = StakeData(amount=100.0, duration=30, network="ethereum")
    data.amount = 200.0
    assert data.amount == 200.0


def test_invalid_amount_assignment_raises_error():
    data = StakeData(amount=100.0, duration=30, network="ethereum")
    mocker.patch('src.validator.validate_stake_amount', return_value=False)
    with pytest.raises(ValidationError):
        data.amount = -50.0


def test_start_date_none_by_default():
    data = StakeData(amount=100.0, duration=30, network="ethereum")
    assert data.start_date is None


def test_start_date_accepts_datetime():
    test_date = datetime(2023, 1, 1, 12, 0, 0)
    data = StakeData(
        amount=100.0,
        duration=30,
        network="ethereum",
        start_date=test_date
    )
    assert data.start_date == test_date


def test_start_date_accepts_none():
    data = StakeData(
        amount=100.0,
        duration=30,
        network="ethereum",
        start_date=None
    )
    assert data.start_date is None


def test_field_validators_gt_constraints():
    with pytest.raises(ValidationError):
        StakeData(amount=0, duration=0, network="ethereum")


def test_field_validators_min_length_constraint():
    with pytest.raises(ValidationError):
        StakeData(amount=100.0, duration=30, network="")