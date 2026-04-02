import argparse
import logging
import sys
from typing import NoReturn
from src.staking_calculator import calculate_staking_reward

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Staking Reward Calculator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--stake_amount",
        type=float,
        required=True,
        help="The amount to stake"
    )
    
    parser.add_argument(
        "--duration",
        type=int,
        required=True,
        help="Staking duration in days"
    )
    
    parser.add_argument(
        "--lockup_percent",
        type=float,
        default=0.0,
        help="Lockup percentage for early withdrawal penalty"
    )
    
    parser.add_argument(
        "--annual_rate",
        type=float,
        default=0.08,
        help="Annual percentage yield rate"
    )
    
    parser.add_argument(
        "--penalty_rate",
        type=float,
        default=0.02,
        help="Penalty rate for early withdrawal"
    )
    
    return parser.parse_args()

def run_calculator(stake_amount: float, duration: int, lockup_percent: float) -> None:
    """Run the staking reward calculation with provided parameters."""
    try:
        if stake_amount <= 0:
            raise ValueError("Stake amount must be positive")
        
        if duration <= 0:
            raise ValueError("Duration must be positive")
            
        if lockup_percent < 0 or lockup_percent > 100:
            raise ValueError("Lockup percent must be between 0 and 100")
            
        # Default values for calculation
        annual_rate = 0.08
        penalty_rate = 0.02
        
        # Calculate the staking reward
        reward = calculate_staking_reward(
            stake_amount, 
            duration, 
            annual_rate, 
            penalty_rate
        )
        
        # Display results
        print(f"Staking Calculation Results:")
        print(f"Stake Amount: ${stake_amount:,.2f}")
        print(f"Duration: {duration} days")
        print(f"Annual Rate: {annual_rate*100:.2f}%")
        print(f"Penalty Rate: {penalty_rate*100:.2f}%")
        print(f"Estimated Reward: ${reward:,.2f}")
        
    except Exception as e:
        logging.error(f"Calculation error: {str(e)}")
        print(f"Error calculating reward: {str(e)}")

def main() -> NoReturn:
    """Main entry point for the CLI."""
    try:
        args = parse_args()
        run_calculator(
            args.stake_amount,
            args.duration,
            args.lockup_percent
        )
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        print(f"Application error: {str(e)}")
        sys.exit(1)
    else:
        sys.exit(0)