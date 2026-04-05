import argparse
import sys
from typing import Tuple
from src.blockchain_client import get_reward_rate
from src.data_fetcher import fetch_data
from src.validator import validate_stake_amount
from src.models.stake_data import StakeData
from src.utils import format_currency, cache_get, cache_set


def calculate_rewards(stake_data: StakeData, reward_rate: float):
    # Simple implementation of reward calculation
    return stake_data.amount * reward_rate


def main() -> int:
    parser = argparse.ArgumentParser(description="Staking Reward Calculator")
    parser.add_argument("--amount", type=float, required=True, help="Stake amount")
    parser.add_argument("--network", required=True, help="Blockchain network name")
    args = parser.parse_args()
    
    # Validate stake amount
    if not validate_stake_amount(args.amount):
        print("Invalid stake amount")
        return 1
    
    # Get reward rate from blockchain
    reward_rate = get_reward_rate(args.network)
    if reward_rate is None:
        print("Invalid reward rate")
        return 1
    
    # Initialize staking data model
    try:
        stake_data = StakeData()
        stake_data.amount = args.amount
        stake_data.network = args.network
    except Exception as e:
        print(f"Error creating stake data: {e}")
        return 1
    
    # Cache the data
    cache_key = f"{stake_data.network}_reward_rate"
    cached_data = cache_get(cache_key)
    
    # Fetch data if not cached
    if cached_data is None:
        data = fetch_data(stake_data.network, stake_data.amount, reward_rate)
        cache_set(cache_key, data)
    
    # Calculate rewards
    rewards = calculate_rewards(stake_data, reward_rate)
    
    # Format the rewards
    formatted_rewards = format_currency(rewards)
    print(f"Estimated rewards: {formatted_rewards}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())