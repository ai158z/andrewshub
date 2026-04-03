import argparse
import sys
import logging
from typing import List, Dict, Any
from src.property_search import search_properties
from src.cli_parser import parse_args
from src.validators import validate_percentage, validate_positive_int, validate_positive_float
from src.utils import convert_to_float, convert_to_int


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def display_properties(properties: List[Dict[str, Any]]) -> None:
    if not properties:
        print("No properties found matching the specified criteria.")
        return

    print(f"Found {len(properties)} properties:")
    for prop in properties:
        print(f"ID: {prop.get('id', 'N/A')}")
        print(f"Address: {prop.get('address', 'N/A')}")
        print(f"Price: {prop.get('price', 'N/A')}")
        print(f"Bedrooms: {prop.get('bedrooms', 'N/A')}")
        print(f"Bathrooms: {prop.get('bathrooms', 'N/A')}")
        print(f"Square Feet: {prop.get('sqft', 'N/A')}")
        print("-" * 30)


def main():
    setup_logging()
    
    try:
        args = parse_args()
    except SystemExit:
        # argparse calls sys.exit() on error, but we want to handle it gracefully
        return 1

    filters = {}
    
    if args.min_price is not None:
        try:
            filters['min_price'] = validate_positive_float(args.min_price)
        except ValueError as e:
            logging.error(f"Invalid minimum price value: {e}")
            return 1
            
    if args.max_price is not None:
        try:
            filters['max_price'] = validate_positive_float(args.max_price)
        except ValueError as e:
            logging.error(f"Invalid maximum price value: {e}")
            return 1
            
    if args.min_bedrooms is not None:
        try:
            filters['min_bedrooms'] = validate_positive_int(args.min_bedrooms)
        except ValueError as e:
            logging.error(f"Invalid minimum bedrooms value: {e}")
            return 1
            
    if args.min_bathrooms is not None:
        try:
            filters['min_bathrooms'] = validate_positive_int(args.min_bathrooms)
        except ValueError as e:
            logging.error(f"Invalid minimum bathrooms value: {e}")
            return 1

    if args.location:
        filters['location'] = args.location
        
    if args.property_type:
        filters['property_type'] = args.property_type

    try:
        properties = search_properties(filters)
        display_properties(properties)
    except Exception as e:
        logging.error(f"Error occurred during property search: {e}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())