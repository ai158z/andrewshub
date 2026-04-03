import math
from decimal import Decimal, getcontext
from typing import Union

# Set precision for decimal calculations
getcontext().prec = 28

def calculate_compound_interest(
    principal: Union[float, Decimal],
    rate: Union[float, Decimal],
    time: Union[float, Decimal],
    compound_frequency: int
) -> Decimal:
    """
    Calculate compound interest based on principal, rate, time, and compound frequency.
    
    Args:
        principal: Initial amount invested
        rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
        time: Time period in years
        compound_frequency: Number of times interest is compounded per year
        
    Returns:
        Decimal: The compound interest amount
    """
    # Convert inputs to Decimal for precision
    principal = Decimal(str(principal))
    rate = Decimal(str(rate))
    time = Decimal(str(time))
    
    # Formula: A = P(1 + r/n)^(nt)
    # Calculate compounded amount
    base = Decimal(1) + (rate / Decimal(compound_frequency))
    exponent = Decimal(compound_frequency) * time
    amount = principal * (base ** exponent)
    
    # Return only the interest portion
    return amount - principal

def apply_compound_interest(
    principal: Union[float, Decimal],
    rate: Union[float, Decimal],
    time: Union[float, Decimal],
    compound_frequency: int
) -> Decimal:
    """
    Apply compound interest to calculate the final amount.
    
    Args:
        principal: Initial amount invested
        rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
        time: Time period in years
        compound_frequency: Number of times interest is compounded per year
        
    Returns:
        Decimal: The final amount after applying compound interest
    """
    # Convert inputs to Decimal for precision
    principal = Decimal(str(principal))
    rate = Decimal(str(rate))
    time = Decimal(str(time))
    
    # Formula: A = P(1 + r/n)^(nt)
    base = Decimal(1) + (rate / Decimal(compound_frequency))
    exponent = Decimal(compound_frequency) * time
    amount = principal * (base ** exponent)
    
    return amount