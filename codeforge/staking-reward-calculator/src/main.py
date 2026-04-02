import argparse
import sys
from typing import List
from src.cli import parse_args, run_calculator
from src.staking_calculator import calculate_apy, calculate_compound_interest, calculate_penalty, calculate_staking_reward


def main() -> int:
    """Main entry point for the staking reward calculator CLI."""
    try:
        args = parse_args()
        return run_calculator(
            args.stake_amount,
            args.duration,
            args.annual_rate,
            args.penalty_rate
        )
    except Exception as e:
        print(f"Error running calculator: {str(e)}")
        return 1
    except KeyboardInterrupt:
        print("Calculator interrupted.")
        return 130  # Standard exit code for script terminated by signal


if __name__ == "__main__":
    sys.exit(main())