import decimal
from decimal import Decimal, getcontext
from typing import Union
import math

# Set precision for decimal calculations
getcontext().prec = 50

Number = Union[int, float, Decimal]

def precise_division(dividend: Number, divisor: Number) -> Decimal:
    """
    Performs high-precision division using Decimal arithmetic.
    
    Args:
        dividend: The number to be divided
        divisor: The number to divide by
        
    Returns:
        The result of the division as a Decimal
        
    Raises:
        decimal.DivisionByZero: If divisor is zero
        TypeError: If inputs are not valid numbers
    """
    if divisor == 0:
        raise decimal.DivisionByZero("Division by zero is not allowed")
    
    try:
        d1 = Decimal(str(dividend))
        d2 = Decimal(str(divisor))
        return d1 / d2
    except Exception as e:
        raise TypeError(f"Invalid input for division: {e}")

def precise_multiply(a: Number, b: Number) -> Decimal:
    """
    Performs high-precision multiplication using Decimal arithmetic.
    
    Args:
        a: First number to multiply
        b: Second number to multiply
        
    Returns:
        The result of the multiplication as a Decimal
        
    Raises:
        TypeError: If inputs are not valid numbers
    """
    try:
        d1 = Decimal(str(a))
        d2 = Decimal(str(b))
        return d1 * d2
    except Exception as e:
        raise TypeError(f"Invalid input for multiplication: {e}")

def percentage_of(amount: Number, percentage: Number) -> Decimal:
    """
    Calculates what percentage of an amount is.
    
    Args:
        amount: The base amount
        percentage: The percentage to calculate
        
    Returns:
        The calculated percentage of the amount as a Decimal
        
    Raises:
        TypeError: If inputs are not valid numbers
    """
    try:
        amount_decimal = Decimal(str(amount))
        percentage_decimal = Decimal(str(percentage))
        # Calculate (amount * percentage) / 100
        return (amount_decimal * percentage_decimal) / Decimal('100')
    except Exception as e:
        raise TypeError(f"Invalid input for percentage calculation: {e}")