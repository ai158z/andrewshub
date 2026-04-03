import math
from typing import Union

def calculate_apy(rate: float, compound_frequency: int) -> float:
    """
    Calculate Annual Percentage Yield (APY) based on nominal rate and compounding frequency.
    
    Args:
        rate: Nominal annual interest rate (as decimal, e.g., 0.05 for 5%)
        compound_frequency: Number of compounding periods per year
        
    Returns:
        APY as a decimal (e.g., 0.05 for 5%)
    """
    if rate < 0 or compound_frequency <= 0:
        raise ValueError("Rate must be non-negative and compound frequency must be positive")
    
    # APY = (1 + r/n)^n - 1
    # where r is rate, n is compound frequency
    apy = (1 + rate / compound_frequency) ** compound_frequency - 1
    return apy

def calculate_compound_interest(
    principal: float,
    rate: float,
    time: float,
    compound_frequency: int
) -> float:
    """
    Calculate compound interest using the formula A = P(1 + r/n)^(nt)
    where:
    - A = final amount
    - P = principal
    - r = annual interest rate (as decimal)
    - n = compound frequency per year
    - t = time in years
    
    Args:
        principal: Initial amount invested
        rate: Annual interest rate (as decimal)
        time: Time period in years
        compound_frequency: Number of compounding periods per year
        
    Returns:
        Final amount after compound interest
    """
    if principal <= 0:
        raise ValueError("Principal must be positive")
    if rate < 0:
        raise ValueError("Rate must be non-negative")
    if time < 0:
        raise ValueError("Time must be non-negative")
    if compound_frequency <= 0:
        raise ValueError("Compound frequency must be positive")
    
    # Compound interest formula: A = P(1 + r/n)^(nt)
    amount = principal * (1 + rate / compound_frequency) ** (compound_frequency * time)
    return amount

def calculate_lockup_penalty(amount: float, penalty_rate: float) -> float:
    """
    Calculate the penalty amount for early withdrawal.
    
    Args:
        amount: The principal amount subject to penalty
        penalty_rate: The penalty rate (as decimal, e.g., 0.10 for 10% penalty)
        
    Returns:
        The penalty amount to be deducted
    """
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if penalty_rate < 0 or penalty_rate > 1:
        raise ValueError("Penalty rate must be between 0 and 1")
    
    penalty = amount * penalty_rate
    return penalty