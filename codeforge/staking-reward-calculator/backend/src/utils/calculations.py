import math
from typing import Dict, Any
from datetime import datetime, timedelta
from decimal import Decimal, getcontext
import logging

# Set precision for decimal calculations
getcontext().prec = 10

def calculate_rewards(stake: float, apr: float, duration: int) -> float:
    """
    Calculate staking rewards based on compound interest formula.
    
    Args:
        stake: Initial amount staked
        apr: Annual percentage rate (as decimal, e.g., 0.05 for 5%)
        duration: Staking period in days
        
    Returns:
        float: Total rewards earned
    """
    if stake < 0 or apr < 0 or duration <= 0:
        raise ValueError("Stake and APR must be non-negative, duration must be positive")
    
    # Compound interest formula: A = P(1 + r/n)^(nt)
    # For staking we assume daily compounding (n=365) for simplicity
    # But we'll use continuous compounding: A = P * e^(r*t)
    # Where t is in years
    time_in_years = duration / 365.0
    final_amount = stake * math.exp(apr * time_in_years)
    return final_amount - stake

def project_rewards(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Project rewards over time with daily compounding.
    
    Args:
        params: Dictionary with keys:
            - initial_stake: Starting stake amount
            - apr: Annual percentage rate
            - duration_days: Number of days to project
            - compounding_frequency: How often rewards compound (daily/weekly/monthly)
            
    Returns:
        dict: Projected rewards at different time intervals
    """
    try:
        # Check if required parameters exist
        if 'initial_stake' not in params or 'apr' not in params:
            raise ValueError("Missing required parameters: initial_stake and/or apr")
            
        initial_stake = float(params.get('initial_stake', 0))
        apr = float(params.get('apr', 0))
        duration_days = int(params.get('duration_days', 365))
        frequency = params.get('compounding_frequency', 'daily')
        
        if initial_stake <= 0 or apr < 0 or duration_days <= 0:
            raise ValueError("Invalid parameters: stake must be positive, APR non-negative, duration positive")
        
        # Calculate daily rewards for the given period
        daily_apr = apr / 365  # Simple daily rate approximation
        
        # For projections, we calculate cumulative rewards at intervals
        daily_projections = {}
        daily_projections['initial'] = initial_stake
        daily_projections['30_days'] = initial_stake * math.exp(daily_apr * 30)
        daily_projections['90_days'] = initial_stake * math.exp(daily_apr * 90)
        daily_projections['180_days'] = initial_stake * math.exp(daily_apr * 180)
        daily_projections['365_days'] = initial_stake * math.exp(daily_apr * 365)
        
        return {
            "total_rewards": float(initial_stake * (math.exp(daily_apr * 365) - 1)),
            "projected_values": daily_projections,
            "final_amount": float(initial_stake * math.exp(daily_apr * 365))
        }
        
    except (KeyError, ValueError, TypeError) as e:
        if isinstance(e, (KeyError, TypeError)):
            raise ValueError(f"Invalid input parameters: {str(e)}")
        else:
            raise e