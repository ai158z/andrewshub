import logging
from typing import Union
from decimal import Decimal, getcontext

# Set precision for decimal calculations
getcontext().prec = 28

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_apy(rate: Union[float, Decimal], days: int) -> Decimal:
    """
    Calculate Annual Percentage Yield (APY) based on a rate and number of days
    
    Args:
        rate: Interest rate (as a decimal, e.g. 0.05 for 5%)
        days: Number of days
        
    Returns:
        APY as a Decimal value
    """
    if days <= 0:
        raise ValueError("Days must be a positive integer")
    
    if rate < 0:
        raise ValueError("Rate cannot be negative")
    
    # APY formula: (1 + rate)^(365/days) - 1
    daily_rate = rate / 365 * days
    apy = (1 + daily_rate) ** (365 / days) - 1
    
    return Decimal(str(apy))

def calculate_compound_interest(principal: Union[float, Decimal], 
                                rate: Union[float, Decimal], 
                                time_in_days: int) -> Decimal:
    """
    Calculate compound interest using the formula: A = P(1 + r/365)^t
    
    Args:
        principal: Initial amount
        rate: Annual interest rate (as a decimal)
        time_in_days: Time period in days
        
    Returns:
        Final amount after compound interest
    """
    if principal < 0:
        raise ValueError("Principal cannot be negative")
    
    if time_in_days < 0:
        raise ValueError("Time cannot be negative")
    
    # Compound interest formula: A = P(1 + r)^t
    # For staking, we use A = P(1 + r/365)^(days)
    rate_per_day = rate / 365
    amount = principal * (1 + rate_per_day) ** time_in_days
    return Decimal(str(amount))

def calculate_penalty(amount: Union[float, Decimal], 
                       penalty_rate: Union[float, Decimal]) -> Decimal:
    """
    Calculate penalty amount based on a given amount and penalty rate
    
    Args:
        amount: The principal amount
        penalty_rate: Penalty rate as a decimal (e.g. 0.05 for 5% penalty)
        
    Returns:
        The penalty amount
    """
    if penalty_rate < 0:
        raise ValueError("Penalty rate cannot be negative")
    
    if amount <= 0:
        logger.warning("Amount should be positive")
    
    penalty = amount * penalty_rate
    return Decimal(str(penalty))

def calculate_staking_reward(stake_amount: Union[float, Decimal], 
                              duration_days: int, 
                              annual_rate: Union[float, Decimal], 
                              penalty_rate: Union[float, Decimal]) -> dict:
    """
    Calculate the staking reward for an amount over a given duration
    
    Args:
        stake_amount: The amount being staked
        duration_days: Duration in days
        annual_rate: Annual interest rate
        penalty_rate: Penalty rate for early withdrawal
        
    Returns:
        Dictionary containing calculated reward information
    """
    if stake_amount <= 0:
        raise ValueError("Stake amount must be positive")
    
    if duration_days <= 0:
        raise ValueError("Duration must be positive")
    
    # Calculate APY first
    apy = calculate_apy(annual_rate, duration_days)
    
    # Calculate reward amount using compound interest
    rate_per_day = annual_rate / 365
    reward = stake_amount * (1 + rate_per_day) ** duration_days
    
    # Calculate penalty amount
    penalty = calculate_penalty(reward, penalty_rate)
    
    return {
        'reward': reward,
        'penalty': penalty,
        'apy': apy
    }