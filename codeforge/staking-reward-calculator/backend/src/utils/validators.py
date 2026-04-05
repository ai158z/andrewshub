import os
import logging
from typing import Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_staking_input(data: dict) -> bool:
    """
    Validate staking input data structure.
    
    Args:
        data: Dictionary containing staking calculation parameters
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Input: stake (float), duration (int), and apr (float) are required
    required_fields = ['stake', 'duration', 'apr']
    field: str
    for field in required_fields:
        if field not in data:
            return False
        if not isinstance(data[field], (int, float)):
            return False
        if data[field] is None:
            return False
    return True

def validate_duration(days: int) -> bool:
    """
    Validate if the duration value is valid.
    
    Args:
        days (int): Number of days to validate
        
    Returns:
        bool: True if valid duration, False otherwise
    """
    if not isinstance(days, int):
        return False
    if days < 0:
        return False
    return True

class StakingInput:
    def __init__(self, stake: float, duration: int, apr: float):
        self.stake = stake
        self.duration = duration
        self.apr = apr

    def is_valid(self) -> bool:
        """Validate staking input fields."""
        return (
            self.stake > 0 and
            self.duration > 0 and
            self.apr > 0
        )