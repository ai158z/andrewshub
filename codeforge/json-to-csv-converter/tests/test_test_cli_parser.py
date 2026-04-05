import pytest
import sys
from unittest.mock import patch
from src.cli_parser import parse_args


def test_parse_args_with_valid_input_output():
    test_args = ['json-to-csv-converter', '--input', 'data.json', '--output', 'output.csv']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == 'data.json'
        assert args['output'] == 'output.csv'


def test_parse_args_with_help_flag():
    test_args = ['json-to-csv-converter', '--help']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as exc_info:
            parse_args()
        assert exc_info.value.code == 0


def test_parse_args_with_missing_input():
    test_args = ['json-to-csv-converter', '--output', 'output.csv']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_missing_output():
    test_args = ['json-to-csv-converter', '--input', 'data.json']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_no_args():
    test_args = ['json-to-csv-converter']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_custom_input_output_paths():
    test_args = ['json-to-csv-converter', '--input', '/path/to/data.json', '--output', '/path/to/output.csv']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == '/path/to/data.json'
        assert args['output'] == '/path/to/output.csv'


def test_parse_args_with_relative_paths():
    test_args = ['json-to-csv-converter', '--input', './data.json', '--output', './output.csv']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == './data.json'
        assert args['output'] == './output.csv'


def test_parse_args_with_nested_paths():
    test_args = ['json-to-csv-converter', '--input', 'dir/data.json', '--output', 'dir/output.csv']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == 'dir/data.json'
        assert args['output'] == 'dir/output.csv'


def test_parse_args_with_explicit_format_flags():
    test_args = ['json-to-csv-converter', '--input', 'data.json', '--output', 'output.csv']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == 'data.json'
        assert args['output'] == 'output.csv'


def test_parse_args_input_and_output_order():
    test_args = ['json-to-csv-converter', '--output', 'output.csv', '--input', 'data.json']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == 'data.json'
        assert args['output'] == 'output.csv'


def test_parse_args_with_empty_input_value():
    test_args = ['json-to-csv-converter', '--input', '', '--output', 'output.csv']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_empty_output_value():
    test_args = ['json-to-csv-converter', '--input', 'data.json', '--output', '']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_input_output_same_file():
    test_args = ['json-to-csv-converter', '--input', 'file.json', '--output', 'file.json']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == 'file.json'
        assert args['output'] == 'file.json'


def test_parse_args_with_multiple_dots_in_filename():
    test_args = ['json-to-csv-converter', '--input', 'data.file.json', '--output', 'output.final.csv']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == 'data.file.json'
        assert args['output'] == 'output.final.csv'


def test_parse_args_with_underscore_in_filename():
    test_args = ['json-to-csv-converter', '--input', 'data_file.json', '--output', 'output_file.csv']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == 'data_file.json'
        assert args['output'] == 'output_file.csv'


def test_parse_args_with_hyphen_in_filename():
    test_args = ['json-to-csv-converter', '--input', 'my-data.json', '--output', 'my-output.csv']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == 'my-data.json'
        assert args['output'] == 'my-output.csv'


def test_parse_args_with_mixed_case_filenames():
    test_args = ['json-to-csv-converter', '--input', 'Data.Json', '--output', 'Output.Csv']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == 'Data.Json'
        assert args['output'] == 'Output.Csv'


def test_parse_args_with_long_input_output_paths():
    test_args = [
        'json-to-csv-converter', 
        '--input', '/very/long/path/to/input/file.json', 
        '--output', '/very/long/path/to/output/file.csv'
    ]
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == '/very/long/path/to/input/file.json'
        assert args['output'] == '/very/long/path/to/output/file.csv'


def test_parse_args_with_special_characters_in_filenames():
    test_args = ['json-to-csv-converter', '--input', 'data_#$@.json', '--output', 'output_#$@.csv']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == 'data_#$@.json'
        assert args['output'] == 'output_#$@.csv'


def test_parse_args_with_whitespace_in_filenames():
    test_args = ['json-to-csv-converter', '--input', 'data file.json', '--output', 'output file.csv']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args['input'] == 'data file.json'
        assert args['output'] == 'output file.csv'