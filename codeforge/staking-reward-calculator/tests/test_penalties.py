import math
from decimal import Decimal, getcontext
from collections import namedtuple

# Set precision for decimal calculations
getcontext().prec = 28

Result = namedtuple('Result', ['compound_rewards', 'penalty_deductions', 'total_reward'])

def calculate_compound_interest(principal, rate, time_in_years, compound_frequency):
    """Calculate compound interest with decimal precision"""
    # Convert to Decimal if not already
    principal = Decimal(str(principal)) if not isinstance(principal, Decimal) else principal
    rate = Decimal(str(rate)) if not isinstance(rate, Decimal) else rate
    time_in_years = Decimal(str(time_in_years)) if not isinstance(time_in_years, Decimal) else time_in_years
    compound_frequency = Decimal(str(compound_frequency)) if not isinstance(compound_frequency, Decimal) else compound_frequency
    
    # Handle compound_frequency = 0 (simple interest case)
    if compound_frequency == 0:
        # Simple interest: A = P(1 + rt)
        amount = principal * (1 + rate * time_in_years)
    else:
        # Compound interest: A = P(1 + r/n)^(nt)
        # Calculate (1 + r/n) first
        base = 1 + rate / compound_frequency
        # Calculate the exponent (n * t)
        exponent = compound_frequency * time_in_years
        # For high precision with Decimals, we need to use math operations
        # that maintain decimal precision
        amount = principal * (base ** exponent)
    
    return amount

def calculate_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency):
    """Calculate staking rewards with penalty calculations"""
    # Validate inputs
    if penalty_rate < 0 or penalty_rate > 1:
        if isinstance(penalty_rate, Decimal):
            if penalty_rate < Decimal('0') or penalty_rate > Decimal('1'):
                raise ValueError("Penalty rate must be between 0 and 1")
        else:
            raise ValueError("Penalty rate must be between 0 and 1")
    
    # Calculate compound interest
    compound_reward = calculate_compound_interest(
        stake_amount, apy, duration/365, compound_frequency
    )
    
    # Calculate penalty deductions
    if isinstance(penalty_rate, Decimal):
        penalty_deductions = compound_reward * penalty_rate
    else:
        penalty_deductions = compound_reward * Decimal(str(penalty_rate)))
    
    # Calculate total reward after penalty
    total_reward = compound_reward - penalty_deductions
    
    return Result(
        compound_rewards=compound_reward,
        penalty_deductions=penalty_deductions,
        total_reward=total_reward
    )

def validate_staking_parameters(stake_amount, duration, apy, penalty_rate, compound_frequency):
    """Validate staking parameters"""
    # Convert to Decimal for comparison if needed
    try:
        if stake_amount < 0:
            return False
        if duration < 0:
            return False
        if apy < 0:
            return False
        if penalty_rate < 0:
            return False
        if penalty_rate > 1:
            return False
        return True
    except:
        return False