import argparse
import sys
import json
import os

def parse_args():
    """Parse command line arguments for the JSON to CSV converter."""
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Input JSON file path')
    parser.add_argument('output_file', help='Output CSV file path')
    parser.add_argument('--field-mapping', help='Field mapping JSON string')
    parser.add_argument('--schema-file', help='Schema definition file path')
    return parser.parse_args()

def main():
    """Entry point for the CLI application that orchestrates the JSON to CSV conversion process."""
    try:
        args = parse_args()
        
        # Convert field mapping from JSON string to dict if provided
        field_mapping = None
        if args.field_mapping:
            field_mapping = json.loads(args.field_mapping)
            
        # Import and validate the conversion
        from src.converter import convert_json_to_csv
        success = convert_json_to_csv(
            input_file=args.input_file,
            output_file=args.output_file,
            field_mapping=field_mapping,
            schema_file=args.schema_file
        )
        
        if not success:
            print("Conversion failed!")
            return 1
            
        print("Conversion completed successfully!")
        return 0
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())