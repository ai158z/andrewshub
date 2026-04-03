import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock
from staking_calculator.calculator import calculate_rewards, calculate_compound_interest
from staking_calculator.models import RewardBreakdown

# Mock the external modules to isolate the calculator logic
@pytest.fixture(autouse=True)
def setup_mocks():
    with patch("staking_calculator.calculator.validate_staking_parameters") as mock_validator, \
         patch("staking_calculator.calculator.calculate_compound_interest") as mock_calculator, \
         patch("staking_calculator.calculator.RewardBreakdown") as mock_breakdown:
        mock_validator.return_value = True
        mock_calculator.return_value = Decimal('100')
        yield mock_validator, mock_calculator, mock_breakdown

def test_calculate_rewards_valid_inputs():
    with patch("staking_calculator.calculator.validate_staking_parameters") as mock_validator, \
         patch("staking_calculator.calculator.calculate_compound_interest") as mock_calculator:
        mock_validator.return_value = True
        mock_calculator.return_value = Decimal('100')
        
        result = calculate_rewards(1000, 365, 0.05, 0.01, 12)
        
        assert isinstance(result, RewardBreakdown)

def test_calculate_rewards_invalid_parameters():
    with patch("staking_calculator.calculator.validate_staking_parameters") as mock_validator:
        mock_validator.return_value = False
        
        with pytest.raises(ValueError, match="Invalid staking parameters provided"):
            calculate_rewards(1000, 365, 0.05, 0.01, 12)

def test_calculate_compound_interest_positive_frequency():
    principal = 1000
    rate = 0.05
    time = 365
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    
    # A = P(1 + r/n)^(nt) - P
    # A = 1000 * (1 + 0.05/12)^(12*1) - 1000
    expected = principal * (1 + rate/compound_frequency) ** (compound_frequency * 1) - principal
    assert result == expected

def test_calculate_compound_interest_zero_frequency():
    principal = 1000
    rate = 0.05
    time = 365
    compound_frequency = 0
    
    with pytest.raises(ValueError, match="Compound frequency must be positive"):
        calculate_compound_interest(principal, rate, time, compound_frequency)

def test_calculate_compound_interest_negative_frequency():
    # This should also raise an error as compound frequency must be positive
    principal = 1000
    rate = 0.05
    time = 365
    compound_frequency = -1
    
    with pytest.raises(ValueError, match="Compound frequency must be positive"):
        calculate_compound_interest(principal, rate, time, compound_frequency)

def test_calculate_compound_interest_edge_case_zero_time():
    principal = 1000
    rate = 0.05
    time = 0
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    expected = principal * (1 + rate/compound_frequency) ** (compound_frequency * 0) - principal
    assert result == expected

def test_calculate_compound_interest_edge_case_zero_rate():
    principal = 1000
    rate = 0
    time = 365
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    expected = principal * (1 + rate/compound_frequency) ** (compound_frequency * 1) - principal
    assert result == expected

def test_calculate_compound_interest_edge_case_zero_principal():
    principal = 0
    rate = 0.05
    time = 365
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    expected = principal * (1 + rate/compound_frequency) ** (compound_frequency * 1) - principal
    assert result == expected

def test_calculate_compound_interest_large_compound_frequency():
    principal = 1000
    rate = 0.05
    time = 365
    compound_frequency = 365
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    expected = principal * (1 + rate/compound_frequency) ** (compound_frequency * 1) - principal
    assert result == expected

def test_calculate_compound_interest_decimal_inputs():
    principal = Decimal('1000.50')
    rate = 0.05
    time = 365
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    expected = float(principal) * (1 + rate/compound_frequency) ** (compound_frequency * 1) - float(principal)
    assert result == expected

def test_calculate_compound_interest_float_inputs():
    principal = 1000.50
    rate = 0.05
    time = 365
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    expected = principal * (1 + rate/compound_frequency) ** (compound_frequency * 1) - principal
    assert result == expected

def test_calculate_compound_interest_int_inputs():
    principal = 1000
    rate = 0.05
    time = 365
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    expected = principal * (1 + rate/compound_frequency) ** (compound_frequency * 1) - principal
    assert result == expected

def test_calculate_compound_interest_time_zero_rate_zero():
    principal = 1000
    rate = 0
    time = 365
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    # When rate is 0, interest should be 0
    assert result == 0

def test_calculate_compound_interest_time_zero_principal_zero():
    principal = 0
    rate = 0.05
    time = 365
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    # When principal is 0, interest should be 0
    assert result == 0

def test_calculate_compound_interest_time_zero_both_zero():
    principal = 0
    rate = 0
    time = 365
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    # When both principal and rate are 0, interest should be 0
    assert result == 0

def test_calculate_compound_interest_time_zero_all_zero():
    principal = 0
    rate = 0
    time = 0
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    # When time is 0, no matter what interest should be 0
    assert result == 0

def test_calculate_compound_interest_time_zero_rate_negative():
    principal = 1000
    rate = -0.05
    time = 365
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    expected = principal * (1 + rate/compound_frequency) ** (compound_frequency * 1) - principal
    assert result == expected

def test_calculate_compound_interest_time_zero_principal_negative():
    principal = -1000
    rate = 0.05
    time = 365
    compound_frequency = 12
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    expected = principal * (1 + rate/compound_frequency) ** (compound_frequency * 1) - principal
    assert result == expected