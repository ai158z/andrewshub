import logging
from typing import Union

logger = logging.getLogger(__name__)

MIN_STAKE_AMOUNT = 0.1
MAX_STAKE_AMOUNT = 1000000.0
MIN_DURATION_DAYS = 1
MAX_DURATION_DAYS = 3650  # 10 years


def validate_stake_amount(amount: Union[int, float]) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The amount to stake
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float)):
        logger.debug("Invalid stake amount type: %s", type(amount))
        return False
        
    if amount < MIN_STAKE_AMOUNT or amount > MAX_STAKE_AMOUNT:
        logger.debug("Stake amount %s out of range [%s, %s]", 
                   amount, MIN_STAKE_AMOUNT, MAX_STAKE_AMOUNT)
        return False
        
    return True


def validate_duration(duration: int) -> bool:
    """
    Validate if the duration is within acceptable range.
    
    Args:
        duration: Duration in days
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(duration, int):
        logger.debug("Invalid duration type: %s", type(duration))
        return False
        
    if duration < MIN_DURATION_DAYS or duration > MAX_DURATION_DAYS:
        logger.debug("Duration %s out of range [%s, %s]", 
                   duration, MIN_DURATION_DAYS, MAX_DURATION_DAYS)
        return False
        
    return True


def validate_inputs(stake_amount: float, duration_days: int, lockup_days: int = 0) -> bool:
    """
    Validate all staking inputs.
    
    Args:
        stake_amount: Amount to stake
        duration_days: Duration of stake in days
        lockup_days: Lockup period in days (default: 0)
        
    Returns:
        bool: True if all inputs are valid, False otherwise
    """
    # Validate stake amount
    if not isinstance(stake_amount, (int, float)) or stake_amount < MIN_STAKE_AMOUNT or stake_amount > MAX_STAKE_AMOUNT:
        return False
    
    # Validate duration
    if not isinstance(duration_days, int) or duration_days < MIN_DURATION_DAYS or duration_days > MAX_DURATION_DAYS:
        return False
        
    # Validate lockup days
    if not isinstance(lockup_days, int) or lockup_days < 0:
        return False
        
    # Additional check: lockup days shouldn't exceed duration
    if lockup_days > duration_days:
        return False
        
    return True