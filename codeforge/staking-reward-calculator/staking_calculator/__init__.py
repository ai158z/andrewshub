from typing import NamedTuple
from decimal import Decimal, getcontext, ROUND_HALF_UP
from .core import calculate_compound_interest, apply_compound_interest
from .models import StakingParameters, RewardBreakdown
from .validators import validate_staking_parameters
from .utils import precise_division, precise_multiply, percentage_of

__version__ = '1.0.0'
__all__ = [
    'calculate_staking_rewards',
    'calculate_compound_interest',
    'apply_compound_interest'
]

# Set precision for Decimal calculations
getcontext().prec = 28
getcontext().rounding = ROUND_HALF_UP

def calculate_staking_rewards(
    stake_amount: Decimal,
    duration: int,
    apy: Decimal,
    compounding_frequency: int,
    penalty_rate: Decimal = Decimal('0')
) -> RewardBreakdown:
    """
    Calculate staking rewards with optional compounding and penalties.
    
    Args:
        stake_amount: The amount staked
        duration: The staking duration in days
        apy: Annual percentage yield (as a decimal, e.g., 0.05 for 5%)
        compounding_frequency: How many times per year to compound (e.g., 1 for annual, 12 for monthly)
        penalty_rate: Penalty rate for early withdrawal (as a decimal, e.g., 0.01 for 1%)
        
    Returns:
        RewardBreakdown: Object containing detailed reward breakdown
    """
    # Validate input parameters
    is_valid = validate_staking_parameters(
        stake_amount, 
        duration, 
        apy, 
        penalty_rate, 
        compounding_frequency
    )
    
    if not is_valid:
        raise ValueError("Invalid staking parameters provided")
    
    # Calculate base rewards with compounding
    principal = float(stake_amount)
    rate = float(apy)
    time_in_years = duration / 365.0
    
    # Calculate compound interest using the formula: A = P(1 + r/n)^(nt)
    # For simplicity in this correction, we'll use a basic implementation
    total_reward = principal * (1 + rate / compounding_frequency) ** (compounding_frequency * time_in_years)
    
    # Calculate compound component of the reward
    compound_rewards = total_reward - principal
    
    # Calculate penalty deductions if applicable
    penalty_deductions = 0
    if penalty_rate > 0:
        penalty_deductions = compound_rewards * float(penalty_rate)
    
    return RewardBreakdown(
        total_reward=Decimal(str(total_reward)),
        compound_rewards=Decimal(str(compound_rewards)),
        penalty_deductions=Decimal(str(penalty_deductions))
    )