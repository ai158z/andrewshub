import math
from decimal import Decimal

def calculate_rewards(principal, apr, duration):
    """Calculate staking rewards using simple interest formula"""
    # Input validation
    if apr < 0:
        raise ValueError("APR cannot be negative")
    
    # Convert inputs to float for calculation
    principal = float(principal)
    apr = float(apr)
    duration = float(duration)
    
    # Simple interest calculation: rewards = principal * apr * duration
    rewards = principal * apr * duration
    
    # Return the total amount (principal + rewards) as a scalar value
    return principal + rewards