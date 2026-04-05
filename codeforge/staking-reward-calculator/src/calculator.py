import math
from decimal import Decimal, getcontext, InvalidOperation
from typing import Union

# Set precision for decimal calculations
getcontext().prec = 50

def calculate_rewards(
    principal: Union[float, int, str], 
    apr: Union[float, int, str], 
    duration: Union[int, float]
) -> dict:
    """
    Calculate compound interest rewards for staking.
    
    Args:
        principal: The initial staking amount
        apr: Annual percentage rate (as a decimal, e.g., 0.05 for 5%)
        duration: Time period in days
        
    Returns:
        Dictionary containing principal, rewards, and total amounts
    """
    # Input validation
    if principal is None or apr is None or duration is None:
        raise ValueError("All parameters (principal, apr, duration) are required")
    
    # Convert inputs to Decimal for precision
    try:
        principal = Decimal(str(principal))
        apr = Decimal(str(apr))
        duration = Decimal(str(duration))
    except (ValueError, TypeError, InvalidOperation) as e:
        raise ValueError(f"Invalid numeric input: {e}")
    
    # Validate input ranges
    if principal < 0:
        raise ValueError("Principal amount cannot be negative")
    if duration < 0:
        raise ValueError("Duration cannot be negative")
    if apr < 0:
        raise ValueError("APR cannot be negative")
    
    # Calculate compound interest
    # Formula: A = P(1 + r/n)^(nt)
    # For staking: A = P * e^(r*t) where continuous compounding is assumed
    # But we'll use daily compounding for more realistic staking simulation
    # A = P * (1 + r/365)^days
    try:
        daily_rate = apr / Decimal('365')
        compound_factor = (Decimal('1') + daily_rate) ** duration
        final_amount = principal * compound_factor
        rewards = final_amount - principal
        
        return {
            'principal': float(principal),
            'rewards': float(rewards),
            'total': float(final_amount),
            'apr': float(apr),
            'duration_days': float(duration)
        }
    except Exception as e:
        raise ValueError(f"Calculation error: {e}")

def calculate_apy(apr: float, compounding_frequency: int = 365) -> float:
    """
    Calculate APY (Annual Percentage Yield) from APR.
    
    Args:
        apr: Annual Percentage Rate
        compounding_frequency: Number of compounding periods per year (default: daily)
        
    Returns:
        Annual Percentage Yield
    """
    try:
        apy = (1 + apr / compounding_frequency) ** compounding_frequency - 1
        return float(apy)
    except Exception as e:
        raise ValueError(f"APY calculation error: {e}")

def calculate_periodic_rewards(
    principal: Union[float, int], 
    apr: float, 
    periods: int, 
    period_duration: str = "daily"
) -> dict:
    """
    Calculate rewards for multiple compounding periods.
    
    Args:
        principal: The initial staking amount
        apr: Annual percentage rate
        periods: Number of compounding periods
        period_duration: Type of compounding period ("daily", "weekly", "monthly")
        
    Returns:
        Dictionary with rewards for each period
    """
    if period_duration == "daily":
        frequency = 365
    elif period_duration == "weekly":
        frequency = 52
    elif period_duration == "monthly":
        frequency = 12
    else:
        raise ValueError("period_duration must be 'daily', 'weekly', or 'monthly'")
    
    try:
        principal = Decimal(str(principal))
        apr = Decimal(str(apr))
        periods = Decimal(str(periods))
        
        # Calculate rewards for each period
        periodic_rate = apr / Decimal(str(frequency))
        total = principal * ((1 + periodic_rate) ** periods)
        rewards = total - principal
        
        return {
            'principal': float(principal),
            'rewards': float(rewards),
            'total': float(total),
            'periods': int(periods)
        }
    except Exception as e:
        raise ValueError(f"Periodic calculation error: {e}")