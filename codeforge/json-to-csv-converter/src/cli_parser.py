import click
import json
import os
from typing import Dict, Any
from src.converter import convert_json_to_csv
from src.validators import is_valid_json_file


def validate_input_file(ctx: click.Context, param: click.Parameter, value: str) -> str:
    """Validate that the input file exists and is a valid JSON file."""
    if not os.path.exists(value):
        raise click.BadParameter(f"Input file '{value}' does not exist.")
    
    if not is_valid_json_file(value):
        raise click.BadParameter(f"Input file '{value}' is not a valid JSON file.")
        
    return value


def validate_schema_file(ctx: click.Context, param: click.Parameter, value: str) -> str:
    """Validate that the schema file exists and is valid if provided."""
    if value and not os.path.exists(value):
        raise click.BadParameter(f"Schema file '{value}' does not exist.")
        
    return value


def validate_field_mapping(ctx: click.Context, param: click.Parameter, value: str) -> Dict[str, str]:
    """Validate and parse field mapping JSON string."""
    if not value:
        return {}
    
    try:
        mapping = json.loads(value)
        if not isinstance(mapping, dict):
            raise click.BadParameter("Field mapping must be a JSON object.")
        return mapping
    except json.JSONDecodeError as e:
        raise click.BadParameter(f"Invalid JSON in field mapping: {str(e)}")


@click.command()
@click.option(
    '-i', '--input-file',
    required=True,
    callback=validate_input_file,
    help='Path to input JSON file'
)
@click.option(
    '-o', '--output-file',
    required=True,
    type=click.Path(dir_okay=False),
    help='Path to output CSV file'
)
@click.option(
    '-m', '--field-mapping',
    callback=validate_field_mapping,
    help='JSON string with field mapping (e.g., \'{"old_name": "new_name"}\')'
)
@click.option(
    '-s', '--schema-file',
    callback=validate_schema_file,
    type=click.Path(exists=True),
    help='Path to JSON schema file for validation'
)
@click.option(
    '-f', '--flatten-separator',
    default='_',
    help='Separator for flattening nested objects (default: "_")'
)
def parse_args(input_file: str, output_file: str, field_mapping: dict, schema_file: str, flatten_separator: str) -> Dict[str, Any]:
    """Parse command line arguments and return as dictionary."""
    return {
        'input_file': input_file,
        'output_file': output_file,
        'field_mapping': field_mapping or {},
        'schema_file': schema_file,
        'flatten_separator': flatten_separator
    }


@parse_args.callback
def main(input_file: str, output_file: str, field_mapping: dict, schema_file: str, flatten_separator: str):
    """Main entry point for the CLI."""
    try:
        # Parse the arguments using click
        parsed_args = {
            'input_file': input_file,
            'output_file': output_file,
            'field_mapping': field_mapping or {},
            'schema_file': schema_file,
            'flatten_separator': flatten_separator
        }
        
        # Perform the conversion
        success = convert_json_to_csv(
            input_file=parsed_args['input_file'],
            output_file=parsed_args['output_file'],
            field_mapping=parsed_args['field_mapping'],
            schema_file=parsed_args['schema_file']
        )
        
        if success:
            click.echo(f"Successfully converted {parsed_args['input_file']} to {parsed_args['output_file']}")
        else:
            raise click.ClickException("Conversion failed")
            
    except Exception as e:
        raise click.ClickException(f"Error during conversion: {str(e)}")


if __name__ == '__main__':
    parse_args()