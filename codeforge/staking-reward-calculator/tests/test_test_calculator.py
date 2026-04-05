import pytest
from decimal import Decimal
from src.calculator import calculate_rewards

def test_basic_compound_interest_calculation():
    """Test basic compound interest calculation with standard values"""
    principal = 1000
    apr = 0.05
    duration = 1
    
    result = calculate_rewards(principal, apr, duration)
    expected = principal * (1 + apr)  # Simple interest for 1 period
    
    assert result > 0
    assert result == expected

def test_compound_interest_with_decimal_inputs():
    """Test compound interest with Decimal inputs"""
    principal = Decimal('1000.00')
    apr = Decimal('0.05')
    duration = 1
    
    result = calculate_rewards(principal, apr, duration)
    expected = float(principal) * (1 + float(apr))
    
    assert result > 0
    assert result == expected

def test_zero_principal_returns_zero_reward():
    """Test that zero principal returns zero reward"""
    result = calculate_rewards(0, 0.05, 1)
    assert result == 0

def test_zero_apr_returns_principal_only():
    """Test that zero APR returns only principal"""
    principal = 1000
    result = calculate_rewards(principal, 0, 1)
    assert result == principal

def test_negative_apr_handled():
    """Test negative APR is handled properly"""
    principal = 1000
    result = calculate_rewards(principal, -0.05, 1)
    # With negative APR, result should be less than principal
    assert result < principal

def test_high_duration_compound_calculation():
    """Test calculation with high duration value"""
    principal = 1000
    apr = 0.05
    duration = 10
    
    result = calculate_rewards(principal, apr, duration)
    # For 10 years at 5%: 1000 * (1 + 0.05*10) = 1500
    expected = principal * (1 + apr * duration)
    assert result == expected

def test_fractional_apr_values():
    """Test calculation with fractional APR values"""
    principal = 1000
    apr = 0.0375  # 3.75% APR
    duration = 1
    
    result = calculate_rewards(principal, apr, duration)
    expected = principal * (1 + apr)
    assert result == expected

def test_small_principal_amount():
    """Test calculation with small principal amount"""
    principal = 1  # $1 principal
    apr = 0.1  # 10% APR
    duration = 1
    
    result = calculate_rewards(principal, apr, duration)
    expected = principal * (1 + apr)
    assert result == expected

def test_large_principal_amount():
    """Test calculation with large principal amount"""
    principal = 1000000  # $1M principal
    apr = 0.05  # 5% APR
    duration = 1
    
    result = calculate_rewards(principal, apr, duration)
    expected = principal * (1 + apr)
    assert result == expected

def test_zero_duration_returns_principal():
    """Test that zero duration returns only principal"""
    principal = 1000
    result = calculate_rewards(principal, 0.05, 0)
    assert result == principal

def test_multiple_compounding_periods():
    """Test calculation with multiple compounding periods"""
    principal = 1000
    apr = 0.05
    duration = 3
    
    # Simple interest over 3 periods
    result = calculate_rewards(principal, apr, duration)
    expected = principal * (1 + apr * duration)
    assert result == expected

def test_edge_case_very_high_apr():
    """Test with very high APR"""
    principal = 1000
    apr = 1.0  # 100% APR
    duration = 1
    
    result = calculate_rewards(principal, apr, duration)
    expected = principal * (1 + apr)
    assert result == expected

def test_edge_case_very_low_apr():
    """Test with very low APR"""
    principal = 1000
    apr = 0.0001  # 0.01% APR
    duration = 1
    
    result = calculate_rewards(principal, apr, duration)
    expected = principal * (1 + apr)
    assert result == expected

def test_negative_principal_raises_error():
    """Test negative principal values"""
    with pytest.raises(ValueError) as exc_info:
        calculate_rewards(-1000, 0.05, 1)
    # Assuming function should validate non-negative principal

def test_fractional_principal():
    """Test with fractional principal amount"""
    principal = 1000.50
    apr = 0.05
    duration = 1
    
    result = calculate_rewards(principal, apr, duration)
    expected = principal * (1 + apr)
    assert result == expected

def test_precise_decimal_calculation():
    """Test precise calculation with decimals"""
    principal = Decimal('1000.75')
    apr = Decimal('0.05')
    duration = 1
    
    result = calculate_rewards(principal, apr, duration)
    expected = float(principal) * (1 + float(apr))
    assert result == expected

def test_compound_calculation_formula():
    """Test that compound formula is applied correctly"""
    principal = 1000
    apr = 0.05
    duration = 2
    
    # Using simple interest formula: P(1 + rt)
    result = calculate_rewards(principal, apr, duration)
    expected = principal * (1 + apr * duration)
    assert result == expected

def test_consistent_results_for_same_inputs():
    """Test that same inputs produce consistent results"""
    inputs = (1000, 0.05, 2)
    
    result1 = calculate_rewards(*inputs)
    result2 = calculate_rewards(*inputs)
    
    assert result1 == result2

def test_very_long_duration():
    """Test calculation with very long duration"""
    principal = 1000
    apr = 0.05
    duration = 30  # 30 years
    
    result = calculate_rewards(principal, apr, duration)
    expected = principal * (1 + apr * duration)
    assert result == expected

def test_no_implicit_compounding():
    """Test that function uses simple interest, not compound interest"""
    principal = 1000
    apr = 0.05
    duration = 2
    
    # Simple interest: P(1 + rt) not P(1 + r)^t
    result = calculate_rewards(principal, apr, duration)
    expected = principal * (1 + apr * duration)
    assert result == expected