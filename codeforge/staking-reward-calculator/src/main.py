import logging
import sys
from src.cli import parse_args, run_calculations

def main() -> None:
    """Main entry point for the staking reward calculator CLI."""
    try:
        args = parse_args()
        run_calculations(args)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()