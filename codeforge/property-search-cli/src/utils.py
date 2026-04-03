import logging
from typing import Union

logger = logging.getLogger(__name__)

def convert_to_float(value: str) -> float:
    """
    Convert a string value to a float.
    
    Args:
        value (str): String representation of a number
        
    Returns:
        float: The converted float value
        
    Raises:
        ValueError: If the string cannot be converted to float
        TypeError: If the input is not a string
    """
    if not isinstance(value, str):
        logger.error(f"Invalid input type: {type(value)}, expected str")
        raise TypeError(f"Expected string input, got {type(value)}")
        
    if not value:
        logger.error("Empty string provided for float conversion")
        raise ValueError("Cannot convert empty string to float")
        
    try:
        result = float(value)
        logger.debug(f"Successfully converted '{value}' to float {result}")
        return result
    except ValueError as e:
        logger.error(f"Failed to convert '{value}' to float: {e}")
        raise ValueError(f"Cannot convert '{value}' to float") from e

def convert_to_int(value: str) -> int:
    """
    Convert a string value to an integer.
    
    Args:
        value (str): String representation of a number
        
    Returns:
        int: The converted integer value
        
    Raises:
        ValueError: If the string cannot be converted to integer
        TypeError: If the input is not a string
    """
    if not isinstance(value, str):
        logger.error(f"Invalid input type: {type(value)}, expected str")
        raise TypeError(f"Expected string input, got {type(value)}")
        
    if not value:
        logger.error("Empty string provided for integer conversion")
        raise ValueError("Cannot convert empty string to integer")
        
    # First try to convert to float to handle "1.0" -> 1 conversion
    try:
        float_val = float(value)
        # Check if it's a whole number
        if float_val != int(float_val):
            logger.error(f"Cannot convert '{value}' to integer - contains non-integer decimal part")
            raise ValueError(f"Cannot convert '{value}' to integer")
        result = int(float_val)
        logger.debug(f"Successfully converted '{value}' to int {result}")
        return result
    except ValueError as e:
        logger.error(f"Failed to convert '{value}' to int: {e}")
        raise ValueError(f"Cannot convert '{value}' to integer") from e