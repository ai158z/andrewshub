"""
Type definitions and conversion functions for financial inputs.
"""

from decimal import Decimal, InvalidOperation
from typing import Union
import re


def to_float(value: Union[str, int, float, Decimal]) -> float:
    """
    Convert a value to float, with strict validation for financial inputs.
    
    Args:
        value: Input value to convert to float
        
    Returns:
        float: The converted float value
        
    Raises:
        ValueError: If the value cannot be converted to float or contains invalid characters
    """
    if isinstance(value, (int, float)):
        return float(value)
    
    if isinstance(value, str):
        # Remove whitespace and check for valid format
        cleaned_value = value.strip()
        
        # Check if it's a valid decimal number format
        if not re.match(r'^-?\d*\.?\d*([eE][+-]?\d+)?$', cleaned_value):
            raise ValueError(f"Invalid number format: {value}")
        
        try:
            return float(cleaned_value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert {value} to float") from e
    
    if isinstance(value, Decimal):
        return float(value)
    
    raise TypeError(f"Unsupported type for conversion to float: {type(value)}")


def to_int(value: Union[str, int, float, Decimal]) -> int:
    """
    Convert a value to integer, with validation.
    
    Args:
        value: Input value to convert to integer
        
    Returns:
        int: The converted integer value
        
    Raises:
        ValueError: If the value cannot be converted to integer or contains fractional parts
    """
    if isinstance(value, int):
        return value
    
    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        else:
            raise ValueError(f"Cannot convert fractional number {value} to integer")
    
    if isinstance(value, str):
        # Remove whitespace
        cleaned_value = value.strip()
        
        # Check if it's a valid integer format
        if re.match(r'^-?\d+$', cleaned_value):
            try:
                return int(cleaned_value)
            except (ValueError, TypeError) as e:
                raise ValueError(f"Cannot convert {value} to integer") from e
        else:
            # If it's not a simple integer, try to parse as float
            try:
                float_val = float(cleaned_value)
                if float_val.is_integer():
                    return int(float_val)
                else:
                    raise ValueError(f"Cannot convert fractional number {value} to integer")
            except ValueError:
                raise ValueError(f"Invalid integer format: {value}")
    
    if isinstance(value, Decimal):
        if value % 1 == 0:
            return int(value)
        else:
            raise ValueError(f"Cannot convert fractional Decimal {value} to integer")
    
    raise TypeError(f"Unsupported type for conversion to integer: {type(value)}")