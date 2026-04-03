import argparse
from typing import Union
import logging
from src.types import to_float, to_int

logger = logging.getLogger(__name__)

def validate_principal(amount: Union[str, float, int]) -> float:
    """
    Validate and convert principal amount to float.
    
    Args:
        amount: Principal amount to validate
        
    Returns:
        float: Validated principal amount
        
    Raises:
        argparse.ArgumentTypeError: If amount is invalid
        ValueError: If amount is not a positive number
    """
    try:
        principal = to_float(amount)
        if principal <= 0:
            raise argparse.ArgumentTypeError(f"Principal amount must be positive, got: {principal}")
        return principal
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid principal amount: {amount}. Error: {str(e)}")

def validate_apr(rate: Union[str, float, int]) -> float:
    """
    Validate and convert APR rate to float.
    
    Args:
        rate: APR rate to validate
        
    Returns:
        float: Validated APR rate
        
    Raises:
        argparse.ArgumentTypeError: If rate is invalid
        ValueError: If rate is not between 0 and 1
    """
    try:
        apr = to_float(rate)
        if apr < 0 or apr > 1:
            raise argparse.ArgumentTypeError(f"APR rate must be between 0 and 1, got: {apr}")
        return apr
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid APR rate: {rate}. Error: {str(e)}")

def convert_input(value: str) -> Union[str, int, float]:
    """
    Convert input value to appropriate type (int, float, or str).
    
    Args:
        value: Input value to convert
        
    Returns:
        Union[str, int, float]: Converted value
    """
    # Try to convert to int first
    try:
        result = to_int(value)
        return result
    except (ValueError, argparse.ArgumentTypeError):
        pass
    
    # Try to convert to float
    try:
        result = to_float(value)
        return result
    except (ValueError, argparse.ArgumentTypeError):
        pass
    
    # Return as string if conversion fails
    return value