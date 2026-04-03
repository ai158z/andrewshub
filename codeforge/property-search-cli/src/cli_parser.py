import argparse
import sys
from typing import Any, Dict, List, Optional
from src.validators import validate_percentage, validate_positive_int, validate_positive_float
from src.utils import convert_to_float, convert_to_int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Property Search CLI - Search for properties based on various filters",
        prog="property-search",
        # Removed allow_abbrev parameter as it's not supported in older Python versions
    )

    # Location filters
    parser.add_argument(
        "--location",
        type=str,
        help="Location to search in (city, state, or zip code)"
    )

    parser.add_argument(
        "--latitude",
        type=validate_positive_float,
        help="Latitude of the center point for radius search"
    )

    parser.add_argument(
        "--longitude",
        type=validate_positive_float,
        help="Longitude of the center point for radius search"
    )

    parser.add_argument(
        "--radius",
        type=validate_positive_float,
        help="Search radius in miles"
    )

    # Price filters
    parser.add_argument(
        "--min-price",
        type=convert_to_int,
        help="Minimum property price"
    )

    parser.add_argument(
        "--max-price",
        type=convert_to_int,
        help="Maximum property price"
    )

    # Property details
    parser.add_argument(
        "--beds",
        type=validate_positive_int,
        help="Number of bedrooms"
    )

    parser.add_argument(
        "--baths",
        type=validate_positive_float,
        help="Number of bathrooms"
    )

    parser.add_argument(
        "--min-sqft",
        type=convert_to_int,
        help="Minimum square footage"
    )

    parser.add_argument(
        "--property-type",
        type=str,
        choices=["house", "apartment", "condo", "townhouse"],
        help="Type of property"
    )

    # Financial filters
    parser.add_argument(
        "--down-payment",
        type=convert_to_int,
        help="Down payment amount"
    )

    parser.add_argument(
        "--down-payment-percent",
        type=validate_percentage,
        help="Down payment percentage (0-100)"
    )

    parser.add_argument(
        "--interest-rate",
        type=validate_percentage,
        help="Interest rate for mortgage calculation"
    )

    parser.add_argument(
        "--loan-term",
        type=validate_positive_int,
        choices=[10, 15, 20, 30],
        help="Loan term in years"
    )

    # Additional filters
    parser.add_argument(
        "--hoa-max",
        type=convert_to_int,
        help="Maximum HOA fees"
    )

    parser.add_argument(
        "--year-built-min",
        type=validate_positive_int,
        help="Minimum year built"
    )

    parser.add_argument(
        "--parking-spaces",
        type=validate_positive_int,
        help="Minimum number of parking spaces"
    )

    # Sort and limit options
    parser.add_argument(
        "--sort-by",
        type=str,
        choices=["price", "sqft", "beds", "baths"],
        help="Sort results by field"
    )

    parser.add_argument(
        "--sort-order",
        type=str,
        choices=["asc", "desc"],
        default="asc",
        help="Sort order"
    )

    parser.add_argument(
        "--limit",
        type=validate_positive_int,
        help="Limit number of results"
    )

    # Output options
    parser.add_argument(
        "--output-format",
        type=str,
        choices=["json", "csv", "table"],
        default="table",
        help="Output format"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    # Validate argument dependencies
    args = parser.parse_args()

    # Validate that if latitude/longitude/radius are used, all three are provided
    if (args.latitude is not None or args.longitude is not None or args.radius is not None) and \
       (args.latitude is None or args.longitude is None or args.radius is None):
        parser.error("--latitude, --longitude, and --radius must be used together")

    # Validate that min_price <= max_price
    if args.min_price is not None and args.max_price is not None:
        if args.min_price > args.max_price:
            parser.error("Minimum price cannot be greater than maximum price")

    # Validate down payment arguments
    if args.down_payment is not None and args.down_payment_percent is not None:
        parser.error("Only one of --down-payment or --down-payment-percent can be specified")

    return args


if __name__ == "__main__":
    # This is for testing purposes
    try:
        parsed_args = parse_args()
        print(parsed_args)
    except SystemExit:
        pass  # argparse calls sys.exit() on error, which is expected behavior