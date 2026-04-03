import logging
from decimal import Decimal, getcontext
from typing import Union
from staking_calculator.models import RewardBreakdown
from staking_calculator.validators import validate_staking_parameters

# Set precision for decimal calculations
getcontext().prec = 28

logger = logging.getLogger(__name__)

def calculate_rewards(
    stake_amount: Union[Decimal, float, int],
    duration: int,
    apy: float,
    penalty_rate: float,
    compound_frequency: int
) -> RewardBreakdown:
    """
    Calculate staking rewards with compound interest and penalties.
    
    Args:
        stake_amount: The principal amount staked
        duration: The staking duration in days
        apy: Annual percentage yield as a decimal (e.g., 0.05 for 5%)
        penalty_rate: Penalty rate as a decimal
        compound_frequency: Number of times interest is compounded per year
        
    Returns:
        RewardBreakdown object containing detailed reward information
    """
    # Validate inputs
    if not validate_staking_parameters(stake_amount, duration, apy, penalty_rate, compound_frequency):
        raise ValueError("Invalid staking parameters provided")
    
    # Convert to Decimal for precision
    stake_amount = Decimal(str(stake_amount))
    apy = Decimal(str(apy))
    penalty_rate = Decimal(str(penalty_rate))
    
    # Calculate compound interest
    compound_reward = calculate_compound_interest(
        float(stake_amount),
        float(apy),
        duration,
        compound_frequency
    )
    
    # Calculate penalty
    penalty_amount = stake_amount * penalty_rate
    
    # Calculate total reward
    total_reward = compound_reward - penalty_amount
    
    return RewardBreakdown(
        total_reward=total_reward,
        compound_rewards=compound_reward,
        penalty_deductions=penalty_amount
    )

def calculate_compound_interest(
    principal: Union[Decimal, float, int],
    rate: float,
    time: int,
    compound_frequency: int
) -> Decimal:
    """
    Calculate compound interest using the formula:
    A = P(1 + r/n)^(nt)
    Where:
    A = final amount
    P = principal
    r = rate (annual)
    n = compound frequency
    t = time in years
    
    Args:
        principal: The initial amount
        rate: The annual interest rate (as decimal)
        time: Time period in days
        compound_frequency: Number of times interest is compounded per year
    """
    if compound_frequency <= 0:
        raise ValueError("Compound frequency must be positive")
    
    principal = Decimal(str(principal))
    rate = Decimal(str(rate))
    
    # Convert time from days to years for the formula
    time_in_years = time / 365
    
    # A = P(1 + r/n)^(nt)
    # For our purposes, we'll calculate based on compound_frequency
    if compound_frequency > 0:
        # Calculate compound interest: A = P(1 + r/n)^(nt)
        # Where n is compound frequency, t is time in years
        amount = principal * (1 + rate / compound_frequency) ** (compound_frequency * time_in_years)
        return amount - principal
    
    return principal * rate * time_in_years