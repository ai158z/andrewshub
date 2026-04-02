import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock
import sys
import os

# Add the path manipulation to make imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
try:
    from src.staking_calculator import (
        calculate_apy, 
        calculate_compound_interest, 
        calculate_lockup_penalty, 
        validate_inputs
    )
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from src.staking_calculator import (
        calculate_apy, 
        calculate_compound_interest, 
        calculate_lockup_penalty, 
        validate_inputs
    )

class TestCalculateApy:
    def test_calculate_apy_normal_case(self):
        result = calculate_apy(Decimal('0.05'), 365)
        assert isinstance(result, Decimal)
        assert result >= 0

    def test_calculate_py_high_rate(self):
        result = calculate_apy(Decimal('1.0'), 365)
        assert isinstance(result, Decimal)

class TestCalculateCompoundInterest:
    def test_compound_interest_normal_case(self):
        principal = Decimal('1000')
        rate = Decimal('0.05')
        result = calculate_compound_interest(principal, rate, 1, 12)
        assert isinstance(result, Decimal)
        assert result > principal

    def test_compound_interest_zero_principal(self):
        result = calculate_compound_interest(Decimal('0'), Decimal('0.05'), 1, 12)
        assert result == Decimal('0')

    def test_compound_interest_zero_rate(self):
        result = calculate_compound_interest(Decimal('1000'), Decimal('0'), 1, 12)
        assert result == Decimal('1000')

    def test_compound_interest_negative_principal(self):
        with pytest.raises(ValueError):
            calculate_compound_interest(Decimal('-1000'), Decimal('0.05'), 1, 12)

    def test_compound_interest_negative_rate(self):
        with pytest.raises(ValueError):
            calculate_compound_interest(Decimal('1000'), Decimal('-0.05'), 1, 12)

class TestCalculateLockupPenalty:
    def test_lockup_penalty_normal_case(self):
        result = calculate_lockup_penalty(Decimal('1000'), Decimal('0.02'))
        assert result == Decimal('20')

    def test_lockup_penalty_zero_amount(self):
        result = calculate_lockup_penalty(Decimal('0'), Decimal('0.02'))
        assert result == Decimal('0')

    def test_lockup_penalty_zero_rate(self):
        result = calculate_lockup_penalty(Decimal('1000'), Decimal('0'))
        assert result == Decimal('0')

    def test_lockup_penalty_negative_amount(self):
        with pytest.raises(ValueError):
            calculate_lockup_penalty(Decimal('-1000'), Decimal('0.02'))

class TestValidateInputs:
    def test_validate_inputs_normal_case(self):
        # This should not raise any exception
        validate_inputs(Decimal('1000'), Decimal('0.05'), 365, 12)

    def test_validate_inputs_negative_principal(self):
        with pytest.raises(ValueError):
            validate_inputs(Decimal('-1000'), Decimal('0.05'), 365, 12)

    def test_validate_inputs_negative_rate(self):
        with pytest.raises(ValueError):
            validate_inputs(Decimal('1000'), Decimal('-0.05'), 365, 12)

    def test_validate_inputs_negative_time(self):
        with pytest.raises(ValueError):
            validate_inputs(Decimal('1000'), Decimal('0.05'), -1, 12)

    def test_validate_inputs_negative_compound_frequency(self):
        with pytest.raises(ValueError):
            validate_inputs(Decimal('1000'), Decimal('0.05'), 365, -1)