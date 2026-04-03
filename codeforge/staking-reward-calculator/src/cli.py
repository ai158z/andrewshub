import argparse
import sys
import logging
from typing import Union
import os

from src.staking_calculator import calculate_apy, calculate_compound_interest, calculate_lockup_penalty
from src.validator import validate_principal, validate_apr, convert_input
from src.types import to_float, to_int

def parse_args():
    parser = argparse.ArgumentParser(
        description="Staking reward calculator for estimating staking returns"
    )
    
    parser.add_argument(
        "--principal",
        type=to_float,
        required=True,
        help="Principal amount to stake"
    )
    
    parser.add_argument(
        "--apr",
        type=to_float,
        required=True,
        help="Annual Percentage Rate (APR) as a decimal (e.g., 0.05 for 5%)"
    )
    
    parser.add_argument(
        "--duration",
        type=to_int,
        required=True,
        help="Duration in days"
    )
    
    parser.add_argument(
        "--compound-frequency",
        type=to_int,
        default=365,
        help="Compound frequency per year (default: 365)"
    )
    
    parser.add_argument(
        "--lockup-penalty",
        type=to_float,
        default=0.0,
        help="Penalty rate for early withdrawal (default: 0.0)"
    )
    
    return parser

def run_calculations(args):
    # Validate inputs
    validate_principal(args.principal)
    validate_apr(args.apr)
    
    # Calculate APY
    apy = calculate_apy(args.apr, args.compound_frequency)
    
    # Calculate final amount with compound interest
    final_amount = calculate_compound_interest(
        args.principal,
        args.apr,
        args.duration / 365.0,
        args.compound_frequency
    )
    
    # Calculate penalty if any
    penalty_amount = 0
    if args.lockup_penalty > 0:
        penalty_amount = calculate_lockup_penalty(args.principal, args.lockup_penalty)
    
    # Calculate final rewards
    reward = final_amount - args.principal - penalty_amount
    
    return {
        'apy': apy,
        'final_amount': final_amount,
        'penalty': penalty_amount,
        'reward': reward
    }

if __name__ == "__main__":
    # Set up argument parsing for command line usage
    args = parse_args()
    try:
        result = run_calculations(args)
        print(f"APY: {result['apy']}")
        print(f"Final Amount: {result['final_amount']}")
        print(f"Penalty: {result['penalty']}")
        print(f"Reward: {result['reward']}")
    except Exception as e:
        print(f"Error running calculations: {e}")
        sys.exit(1)