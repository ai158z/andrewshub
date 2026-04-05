# Staking Reward Calculator

def calculate_staking_rewards(principal, annual_rate, time_years):
    return principal * (1 + annual_rate) ** time_years

if __name__ == "__main__":
    principal = 1000 # Example: $1000 stake
    annual_rate = 0.15 # 15% annual yield
    time_years = 1
    
    rewards = calculate_staking_rewards(principal, annual_rate, time_years)
    print(f"Estimated staking rewards: ${rewards:.2f}")