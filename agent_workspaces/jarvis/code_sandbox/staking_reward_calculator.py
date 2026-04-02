# Staking Reward Calculator

def calculate_staking_reward(
    principal,
    apr,
    duration_days,
    lockup_penalty=0
):
    # Calculate compound interest
    daily_rate = (apr / 100) / 365
    amount = principal * (1 + daily_rate) ** duration_days
    
    # Apply lockup penalty if applicable
    if lockup_penalty > 0:
        amount *= (1 - lockup_penalty / 100)
    
    return amount