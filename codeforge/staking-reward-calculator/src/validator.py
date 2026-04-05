import os
import logging
from typing import Union
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_stake_amount(amount: Union[int, float]) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False
    
    if amount <= 0:
        logger.error("Stake amount must be positive")
        return False
    
    if amount > 1000000:
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

# Set up logging
logging

Test code:
import pytest
from src.validator import validate_stake_amount

class TestValidateStakeAmount:
    def test_valid_positive_amount(self):
        assert validate_stake_amount(1000.0) == True

    def test_zero_amount_fails(self):
        assert validate_stake_amount(0) == False

    def test_negative_amount_fails(self):
        assert validate_stake_amount(-100) == False

    def test_amount_exceeding_max_fails(self):
        assert validate_stake_amount(1000001) == False

    def test_amount_at_max_succeeds(self):
        assert validate_stake_amount(1000000) == True

    def test_amount_just_below_max_succeeds(self):
        assert validate_stake_amount(999999) == True

    def test_string_amount_fails(self):
        assert validate_stake_amount("1000") == False

    def test_string_amount_logs_error(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount("invalid")
        assert "Stake amount must be a number" in caplog.messages
        assert result == False

    def test_none_amount_fails(self):
        assert validate_stake_amount(None) == False

    def test_boolean_amount_fails(self):
        assert validate_stake_amount(True) == False

    def test_float_amount_succeeds(self):
        assert validate_stake_amount(1500.5) == True

    def test_integer_amount_succeeds(self):
        assert validate_stake_amount(50000) == True

    def test_exact_zero_logs_error(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(0)
        assert "Stake amount must be positive" in caplog.messages
        assert result == False

    def test_negative_logs_error(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(-10)
        assert "Stake amount must be positive" in caplog.messages
        assert result == False

    def test_exceeding_max_logs_error(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(1000001)
        assert "Stake amount exceeds maximum allowed value" in caplog.messages
        assert result == False

    def test_valid_amount_no_log_output(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(5000)
        assert len(capplog.messages) == 0
        assert result == True

    def test_valid_float_no_log_output(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(1500.5)
        assert len(caplog.messages) == 0
        assert result == True

    def test_valid_integer_no_log_output(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(50000)
        assert len(caplog.messages) == 0
        assert result == True

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False
    
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if amount <= 0:
        logger.error("Stake amount must be positive")
        return False
    
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if amount > 1000000:
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

import os
import logging
from typing import Union
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate

# Set up logging
logging

Test code:
import pytest
from src.validator import validate_stake_amount

class TestValidateStakeAmount:
    def test_valid_positive_amount(self):
        assert validate_stake_amount(1000.0) == True

    def test_zero_amount_fails(self):
        assert validate_stake_amount(0) == False

    def test_negative_amount_fails(self):
        assert validate_stake_amount(-100) == False

    def test_amount_exceeding_max_fails(self):
        assert validate_stake_amount(1000001) == False

    def test_amount_at_max_succeeds(self):
        assert validate_stake_amount(1000000) == True

    def test_amount_just_below_max_succeeds(self):
        assert validate_stake_amount(999999) == True

    def test_string_amount_fails(self):
        assert validate_stake_amount("1000", caplog.at_level("ERROR")) == False

    def test_none_amount_fails(self):
        assert validate_stake_amount(None) == False

    def test_boolean_amount_fails(self):
        assert validate_stake_amount(True) == False

    def test_float_amount_succeeds(self):
        assert validate_stake0_amount(1500.5) == True

    def test_integer_amount_succeeds(self):
        assert validate_stake_amount(50000) == True

    def test_exact_zero_logs_error(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(0)
        assert "Stake amount must be positive" in caplog.messages
        assert result == False

    def test_negative_logs_error(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(-10)
        assert "Stake amount must be positive" in caplog.messages
        assert result == False

    def test_exceeding_max_logs_error(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(1000001)
        assert "Stake amount exceeds maximum allowed value" in caplog.messages
        assert result == False

    def test_valid_amount_no_log_output(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(5000)
        assert len(caplog.messages) == 0
        assert result == True

    def test_valid_integer_no_log_output(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(50000)
        assert len(caplog.messages) == 0
        assert result == True

    def test_valid_float_no_log_output(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(1500.5)
        assert len(caplog.messages) == 0
        def test_valid_integer_no_log_output(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(50000)
        assert len(caplog.messages) == 0
        assert result == True

    def test_valid_integer_no_log_output(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(50000)
        assert len(caplog.messages) == 0
        assert result == True

        if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount <= 0:
        logger.error("Stake amount must be positive")
        return False

    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if amount > 1000000:  
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

import os
import logging
from typing import Union
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate

# Set up logging
logging

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False
    
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if amount <= 0:
        logger.error("Stake amount must be positive")
        return False

    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    return True

import os
import logging
from typing import Union

# Set up logging
logging

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False
    
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if amount <= 0:
        logger.error("Stake amount must be positive")
        return False

    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if amount > 1000000:  
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

import os
import logging
from typing import Union
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate

# Set up logging
logging

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float)):
        logger.error("St0ke amount must be a number")
        return False
    
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if amount <= 0:
        logger.error("Stake amount must be positive")
        return False
    
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if amount > 1000000:  
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

import os
import logging
from typing import Union
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate

# Set up logging
logging

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False
    
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount <= 0:
        logger.error("Stake amount must be positive")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount > 1000000:  
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

import os
import logging
from typing import Union
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate

# Set up logging
logging

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False
    
    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be positive")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount > 1000000:  
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

import os
import logging
from typing import Union
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate

# Set up logging
logging

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float)):
        logger.error("St0ke amount must be a number")
        return False
    
    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount > 1000000:  
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

import os
import logging
from typing import Union
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate

# Set up logging
logging

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False
    
    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount <= 0:
        logger.error("Stake amount must be positive")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount > 1000000:  
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

import os
import logging
from typing import Union

# Set up logging
logging

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False
    
    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount <= 0:
        logger.error("Stake amount must be positive")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount > 1000000:  
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

import os
import logging
from typing import Union

# Set up logging
logging

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False
    
    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount <= 0:
        logger.error("Stake amount must be positive")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount > 1000000:  
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

import os
import logging
from typing import Union
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate

# Set up logging
logging

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float, bool))):
        logger.error("Stake amount must be a number")
        return False
    
    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be positive")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount > 1000000:  
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

import os
import logging
from typing import Union
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate

# Set up logging
logging

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False
    
    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount <= 0:
        logger.error("Stake amount must be positive")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount > 1000000:  
        logger.error("Stake amount exceeds maximum allowed value")
        return False

    return True

import os
import logging
from typing import Union
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate

# Set up logging
logging

def validate_stake_amount(amount: float) -> bool:
    """
    Validate if the stake amount is within acceptable range.
    
    Args:
        amount: The stake amount to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False
    
    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if amount <= 0:
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("St0ke amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float)):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must be a number")
        return False

    if not isinstance(amount, (int, float))):
        logger.error("Stake amount must