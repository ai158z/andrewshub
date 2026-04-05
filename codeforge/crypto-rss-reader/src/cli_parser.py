import argparse
import sys
from typing import List


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for the crypto-rss-reader application."""
    parser = argparse.ArgumentParser(
        description="Crypto RSS Reader - A tool for monitoring cryptocurrency news",
        prog="crypto-rss-reader"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file",
        default="config.yaml"
    )
    
    parser.add_argument(
        "--db-path",
        type=str,
        help="Path to SQLite database file",
        default="data.db"
    )
    
    parser.add_argument(
        "--add-feed",
        type=str,
        help="Add a new RSS feed URL to monitor",
        metavar="URL"
    )
    
    parser.add_argument(
        "--list-feeds",
        action="store_true",
        help="List all configured feed URLs"
    )
    
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode"
    )
    
    parser.add_argument(
        "--moonpay-alerts",
        action="store_true",
        help="Enable MoonPay alerts for payment-relevant articles"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    return parser.parse_args()


def display_menu(options: List[str]) -> str:
    """Display a menu and get user selection."""
    if not options:
        raise ValueError("Menu options cannot be empty")
    
    print("\nAvailable options:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    print()
    while True:
        try:
            choice = input("Select an option (enter number): ")
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(options):
                return options[choice_idx]
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            sys.exit(0)