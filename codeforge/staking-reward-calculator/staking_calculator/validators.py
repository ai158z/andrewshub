import decimal
from typing import Union

def validate_staking_parameters(
    stake_amount: Union[int, float, decimal.Decimal],
    duration: Union[int, float, decimal.Decimal],
    apy: Union[int, float, decimal.Decimal],
    penalty_rate: Union[int, float, decimal.Decimal],
    compound_frequency: int
) -> bool:
    """
    Validate staking parameters for reward calculations.
    
    Args:
        stake_amount: The amount being staked
        duration: The staking duration in days
        apy: Annual percentage yield as a percentage (e.g., 5 for 5%)
        penalty_rate: Early withdrawal penalty rate as a percentage
        compound_frequency: How often interest compounds per year
        
    Returns:
        bool: True if all parameters are valid
        
    Raises:
        ValueError: If any parameter is invalid
        TypeError: If any parameter is not of the correct type
    """
    # Validate stake_amount
    if not isinstance(stake_amount, (int, float, decimal.Decimal)):
        raise TypeError("stake_amount must be a number")
    if stake_amount < 0:
        raise ValueError("stake_amount must be non-negative")
        
    # Validate duration
    if not isinstance(duration, (int, float, decimal.Decimal)):
        raise TypeError("duration must be a number")
    if duration < 0:
        raise ValueError("duration must be non-negative")
        
    # Validate APY
    if not isinstance(apy, (int, float, decimal.Decimal)):
        raise TypeError("apy must be a number")
    if apy < 0:
        raise ValueError("apy must be non-negative")
        
    # Validate penalty_rate
    if not isinstance(penalty_rate, (int, float, decimal.Decimal)):
        raise TypeError("penalty_rate must be a number")
    if penalty_rate < 0 or penalty_rate > 100:
        raise ValueError("penalty_rate must be between 0 and 100")
        
    # Validate compound_frequency
    if not isinstance(compound_frequency, int):
        raise TypeError("compound_frequency must be an integer")
    if compound_frequency <= 0:
        raise ValueError("compound_frequency must be positive")
        
    return True