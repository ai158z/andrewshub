import pytest
from unittest.mock import patch, mock_open
import json
import os
from src.cli_parser import validate_input_file, validate_schema_file, validate_field_mapping, parse_args, main
from click import ClickException
from click.testing import CliRunner


def test_validate_input_file_exists_and_valid(tmp_path):
    # Create a valid JSON file for testing
    test_file = tmp_path / "test.json"
    test_file.write_text('{"test": "data"}')
    
    with patch('src.cli_parser.is_valid_json_file', return_value=True):
        result = validate_input_file(None, None, str(test_file))
        assert result == str(test_file)


def test_validate_input_file_not_exists():
    with pytest.raises(Exception):
        validate_input_file(None, None, "nonexistent.json")


def test_validate_input_file_invalid_json(tmp_path):
    test_file = tmp_path / "invalid.json"
    test_file.write_text("{invalid json}")
    
    with patch('src.cli_parser.is_valid_json_file', return_value=False):
        with pytest.raises(ClickException):
            validate_input_file(None, None, str(test_file))


def test_validate_schema_file_exists(tmp_path):
    schema_file = tmp_path / "schema.json"
    schema_file.write_text('{"type": "object"}')
    result = validate_schema_file(None, None, str(schema_file))
    assert result == str(schema_file)


def test_validate_schema_file_not_exists():
    with pytest.raises(ClickException):
        validate_schema_file(None, None, "nonexistent_schema.json")


def test_validate_field_mapping_valid():
    mapping_str = '{"old": "new"}'
    result = validate_field_mapping(None, None, mapping_str)
    assert result == {"old": "new"}


def test_validate_field_mapping_empty():
    result = validate_field_mapping(None, None, None)
    assert result == {}


def test_validate_field_mapping_invalid_json():
    with pytest.raises(ClickException):
        validate_field_mapping(None, None, "{invalid: json}")


def test_validate_field_mapping_not_dict():
    with pytest.raises(ClickException):
        validate_field_mapping(None, None, '"not a dict"')


def test_parse_args_basic():
    result = parse_args(
        input_file="input.json",
        output_file="output.csv",
        field_mapping={"old": "new"},
        schema_file="schema.json",
        flatten_separator="_"
    )
    assert result["input_file"] == "input.json"
    assert result["output_file"] == "output.csv"
    assert result["field_mapping"] == {"old": "new"}
    assert result["schema_file"] == "schema.json"
    assert result["flatten_separator"] == "_"


def test_main_success():
    runner = CliRunner()
    with patch('src.cli_parser.convert_json_to_csv', return_value=True):
        result = runner.invoke(parse_args, [
            '-i', 'test_input.json',
            '-o', 'test_output.csv'
        ])
        assert result.exit_code == 0


def test_main_conversion_failure():
    runner = CliRunner()
    with patch('src.cli_parser.convert_json_to_csv', return_value=False):
        result = runner.invoke(parse_args, [
            '-i', 'test_input.json',
            '-o', 'test_output.csv'
        ])
        assert result.exit_code != 0


def test_main_with_field_mapping():
    runner = CliRunner()
    with patch('src.cli_parser.convert_json_to_csv', return_value=True):
        result = runner.invoke(parse_args, [
            '-i', 'test_input.json',
            '-o', 'test_output.csv',
            '-m', '{"old_field": "new_field"}'
        ])
        assert result.exit_code == 0


def test_main_with_schema():
    runner = CliRunner()
    with patch('src.cli_parser.convert_json_to_csv', return_value=True):
        result = runner.invoke(parse_args, [
            '-i', 'test_input.json',
            '-o', 'test_output.csv',
            '-s', 'schema.json'
        ])
        assert result.exit_code == 0


def test_main_with_flatten_separator():
    runner = CliRunner()
    with patch('src.cli_parser.convert_json_to_csv', return_value=True):
        result = runner.invoke(parse_args, [
            '-i', 'test_input.json',
            '-o', 'test_output.csv',
            '-f', '--'
        ])
        assert result.exit_code == 0


def test_main_missing_required_args():
    runner = CliRunner()
    result = runner.invoke(parse_args, ['-i', 'test.json'])
    assert result.exit_code != 0


def test_main_invalid_field_mapping():
    runner = CliRunner()
    result = runner.invoke(parse_args, [
        '-i', 'test.json',
        '-o', 'output.csv',
        '-m', '{invalid json}'
    ])
    assert result.exit_code != 0


def test_main_file_not_exist():
    runner = CliRunner()
    result = runner.invoke(parse_args, [
        '-i', 'nonexistent.json',
        '-o', 'output.csv'
    ])
    assert result.exit_code != 0


def test_main_schema_not_exist():
    runner = CliRunner()
    result = runner.invoke(parse_args, [
        '-i', 'test.json',
        '-o', 'output.csv',
        '-s', 'nonexistent_schema.json'
    ])
    assert result.exit_code != 0


def test_main_success_with_all_options():
    runner = CliRunner()
    with patch('src.cli_parser.convert_json_to_csv', return_value=True):
        result = runner.invoke(parse_args, [
            '-i', 'input.json',
            '-o', 'output.csv',
            '-m', '{"test": "mapping"}',
            '-s', 'schema.json',
            '-f', '--'
        ])
        assert result.exit_code == 0