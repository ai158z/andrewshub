import logging
from typing import Union
import math

logger = logging.getLogger(__name__)

def calculate_compound_interest(principal: float, rate: float, time: float, frequency: int) -> float:
    """
    Calculate compound interest based on principal, rate, time, and compounding frequency.
    
    Args:
        principal: The initial amount invested
        rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
        time: Time period in years
        frequency: Number of times interest is compounded per year
    
    Returns:
        The compound interest amount
    """
    # Input validation
    if principal < 0:
        raise ValueError("Principal cannot be negative")
    if rate < 0:
        raise ValueError("Rate cannot be negative")
    if time < 0:
        raise ValueError("Time cannot be negative")
    if frequency <= 0:
        raise ValueError("Frequency must be positive")
    if not isinstance(frequency, int):
        raise ValueError("Frequency must be an integer")
    
    logger.debug(f"Calculating compound interest for principal={principal}, rate={rate}, time={time}, frequency={frequency}")
    
    # Compound interest formula: A = P(1 + r/n)^(nt)
    # Where A is the final amount, P is principal, r is rate, n is frequency, t is time
    amount = principal * (1 + rate / frequency) ** (frequency * time)
    
    compound_interest = amount - principal
    logger.info(f"Compound interest calculated: {compound_interest}")
    
    return compound_interest

def calculate_penalty(amount: float, penalty_rate: float) -> float:
    """
    Calculate penalty amount based on the given amount and penalty rate.
    
    Args:
        amount: The amount to calculate penalty on
        penalty_rate: The penalty rate (as decimal, e.g., 0.05 for 5%)
    
    Returns:
        The penalty amount
    """
    # Input validation
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if penalty_rate < 0:
        raise ValueError("Penalty rate cannot be negative")
    if penalty_rate > 1:
        raise ValueError("Penalty rate cannot be greater than 1 (100%)")
    
    logger.debug(f"Calculating penalty for amount={amount}, penalty_rate={penalty_rate}")
    
    penalty = amount * penalty_rate
    logger.info(f"Penalty calculated: {penalty}")
    
    return penalty