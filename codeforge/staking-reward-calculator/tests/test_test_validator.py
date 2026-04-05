import pytest
from src.validator import validate_stake_amount


def test_valid_positive_amount() -> None:
    assert validate_stake_amount(1000.0) is True


def test_zero_amount_fails() -> None:
    assert validate_stake_amount(0.0) is False


def test_negative_amount_fails() -> None:
    assert validate_stake_amount(-100.0) is False


def test_minimum_valid_amount() -> None:
    assert validate_stake_amount(0.01) is True


def test_amount_less_than_minimum_fails() -> None:
    assert validate_stake_amount(-0.01) is False


def test_large_valid_amount() -> None:
    assert validate_stake_amount(50000.0) is True


def test_valid_boundary_amount() -> None:
    assert validate_stake_amount(100.0) is True


def test_decimal_amount() -> None:
    assert validate_stake_amount(1000.50) is True


def test_none_input_fails() -> None:
    with pytest.raises((TypeError, ValueError)):
        validate_stake_amount(None)


def test_string_input_fails() -> None:
    with pytest.raises((TypeError, ValueError)):
        validate_stake_amount("1000")


def test_invalid_type_list_fails() -> None:
    with pytest.raises((TypeError, ValueError)):
        validate_stake_amount([1000])


def test_invalid_type_dict_fails() -> None:
    with pytest.raises((TypeError, ValueError)):
        validate_stake_amount({"amount": 1000})