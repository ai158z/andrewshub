import argparse
from typing import Union
import logging

logger = logging.getLogger(__name__)

def validate_percentage(value: str) -> float:
    """
    Validate and convert a string to a percentage float value (0-100).
    
    Args:
        value: String representation of a percentage value
        
    Returns:
        float: Percentage value between 0 and 100
        
    Raises:
        argparse.ArgumentTypeError: If value is not a valid percentage
    """
    try:
        float_value = float(value)
        
        # Check if it's within percentage range
        if not 0 <= float_value <= 100:
            raise argparse.ArgumentTypeError(
                f"Percentage value must be between 0 and 100, got: {float_value}"
            )
            
        return float_value
    except ValueError as e:
        logger.error(f"Invalid percentage value: {value}")
        raise argparse.ArgumentTypeError(f"Invalid percentage value: {value}") from e

def validate_positive_int(value: str) -> int:
    """
    Validate and convert a string to a positive integer.
    
    Args:
        value: String representation of an integer
        
    Returns:
        int: Positive integer value
        
    Raises:
        argparse.ArgumentTypeError: If value is not a valid positive integer
    """
    try:
        int_value = int(value)
        
        # Check if it's positive
        if int_value < 0:
            raise argparse.ArgumentTypeError(
                f"Value must be a positive integer, got: {int_value}"
            )
            
        return int_value
    except ValueError as e:
        logger.error(f"Invalid positive integer value: {value}")
        raise argparse.ArgumentTypeError(f"Invalid positive integer value: {value}") from e

def validate_positive_float(value: str) -> float:
    """
    Validate and convert a string to a positive float.
    
    Args:
        value: String representation of a float value
        
    Returns:
        float: Positive float value
        
    Raises:
        argparse.ArgumentTypeError: If value is not a valid positive float
    """
    try:
        float_value = float(value)
        
        # Check if it's positive
        if float_value < 0:
            raise argparse.ArgumentTypeError(
                f"Value must be a positive number, got: {float_value}"
            )
            
        return float_value
    except ValueError as e:
        logger.error(f"Invalid positive float value: {value}")
        raise argparse.ArgumentTypeError(f"Invalid positive float value: {value}") from e