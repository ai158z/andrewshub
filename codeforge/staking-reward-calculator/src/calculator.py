import math
from typing import Dict, Union
import logging

logger = logging.getLogger(__name__)

def calculate_rewards(stake_amount: float, duration: int, apy: float, 
                     commission: float) -> Dict[str, Union[float, int]]:
    """
    Calculate staking rewards based on stake amount, duration, APY, and commission.
    
    Args:
        stake_amount: The amount of tokens to stake
        duration: The staking duration in days
        apy: Annual percentage yield (as a decimal, e.g. 0.05 for 5%)
        commission: Validator commission rate (as a decimal, e.g. 0.1 for 10%)
        
    Returns:
        Dictionary containing the calculated rewards data
    """
    # Validate inputs
    if stake_amount <= 0:
        raise ValueError("Stake amount must be positive")
        
    _validate_inputs(stake_amount, duration, apy, commission)
    
    # Calculate reward using compound interest formula
    # Convert APY to daily rate: (1 + apy)^(1/365) - 1
    # But we use the effective rate after commission
    effective_apy = apy * (1 - commission)
    daily_rate = (1 + effective_apy) ** (1/365) - 1
    total_reward = stake_amount * ((1 + daily_rate) ** duration - 1)
    
    return {
        'total_reward': total_reward,
        'duration_days': duration,
        'stake_amount': stake_amount,
        'apy': apy,
        'commission': commission
    }

def _validate_inputs(stake_amount: float, duration: int, apy: float, commission: float) -> None:
    """Validate calculator inputs and raise appropriate errors."""
    if stake_amount < 0:
        raise ValueError("Stake amount cannot be negative")
    if duration < 0:
        raise ValueError("Duration cannot be negative")
    if apy < 0:
        raise ValueError("APY cannot be negative")
    if commission < 0:
        raise ValueError("Commission cannot be negative")
    if apy > 1:
        raise ValueError("APY must be between 0 and 1")
    if commission > 1:
        raise ValueError("Commission must be between 0 and 1")
    if duration == 0:
        raise ValueError("Duration must be positive")