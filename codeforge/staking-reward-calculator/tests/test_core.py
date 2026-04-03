import pytest
from decimal import Decimal
from staking_calculator.core import calculate_compound_interest, apply_compound_interest

def test_calculate_compound_interest_basic():
    result = calculate_compound_interest(1000, 0.05, 2, 4)
    expected = Decimal('102.515625')
    assert result == expected

def test_calculate_compound_interest_zero_principal():
    result = calculate_compound_interest(0, 0.05, 2, 4)
    assert result == Decimal('0')

def test_calculate_compound_interest_zero_rate():
    result = calculate_compound_interest(1000, 0, 2, 4)
    assert result == Decimal('0')

def test_calculate_compound_interest_zero_time():
    result = calculate_compound_interest(1000, 0.05, 0, 4)
    assert result == Decimal('0')

def test_calculate_compound_interest_annual_compounding():
    result = calculate_compound_interest(1000, 0.05, 1, 1)
    expected = Decimal('50')
    assert result == expected

def test_calculate_compound_interest_monthly_compounding():
    result = calculate_compound_interest(1000, 0.05, 1, 12)
    expected = Decimal('51.161896609645917458125')
    assert result == expected

def test_calculate_compound_interest_daily_compounding():
    result = calculate_compound_interest(1000, 0.05, 1, 365)
    expected = Decimal('51.269778594557064615055')
    assert result == expected

def test_calculate_compound_interest_decimal_inputs():
    result = calculate_compound_interest(Decimal('1000'), Decimal('0.05'), Decimal('2'), 4)
    expected = Decimal('102.515625')
    assert result == expected

def test_calculate_compound_interest_fractional_time():
    result = calculate_compound_interest(1000, 0.05, 2.5, 4)
    expected = Decimal('134.825663716814159292035')
    assert result == expected

def test_apply_compound_interest_basic():
    result = apply_compound_interest(1000, 0.05, 2, 4)
    expected = Decimal('1102.515625')
    assert result == expected

def test_apply_compound_interest_zero_principal():
    result = apply_compound_interest(0, 0.05, 2, 4)
    assert result == Decimal('0')

def test_apply_compound_interest_zero_rate():
    result = apply_compound_interest(1000, 0, 2, 4)
    assert result == Decimal('1000')

def test_apply_compound_interest_zero_time():
    result = apply_compound_interest(1000, 0.05, 0, 4)
    assert result == Decimal('1000')

def test_apply_compound_interest_decimal_inputs():
    result = apply_compound_interest(Decimal('1000'), Decimal('0.05'), Decimal('2'), 4)
    expected = Decimal('1102.515625')
    assert result == expected

def test_apply_compound_interest_fractional_time():
    result = apply_compound_interest(1000, 0.05, 2.5, 4)
    expected = Decimal('1134.825663716814159292035')
    assert result == expected

def test_calculate_compound_interest_negative_principal():
    result = calculate_compound_interest(-1000, 0.05, 2, 4)
    expected = Decimal('-102.515625')
    assert result == expected

def test_calculate_compound_interest_negative_rate():
    result = calculate_compound_interest(1000, -0.05, 2, 4)
    expected = Decimal('-97.53021645021645021645022')
    assert result == expected

def test_apply_compound_interest_negative_principal():
    result = apply_compound_interest(-1000, 0.05, 2, 4)
    expected = Decimal('-897.484375')
    assert result == expected

def test_apply_compound_interest_negative_rate():
    result = apply_compound_interest(1000, -0.05, 2, 4)
    expected = Decimal('902.46978354978354978355')
    assert result == expected

def test_calculate_compound_interest_high_frequency():
    result = calculate_compound_interest(1000, 0.05, 1, 1000)
    expected = Decimal('51.271073839245847410635')
    assert result == expected