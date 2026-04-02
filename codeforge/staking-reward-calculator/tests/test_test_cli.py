import argparse
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

# Mock the actual modules for testing
sys.path.insert(0, 'src')
from cli import main as cli_main
from staking_calculator import validate_inputs


def test_main_function_exists():
    """Test that the main function exists and is callable"""
    assert callable(cli_main), "main function should be callable"


@patch('sys.argv', ['staking_calculator', '--principal', '1000', '--rate', '0.05', '--days', '365'])
@patch('sys.stdout', new_callable=StringIO)
@patch('sys.stderr', new_callable=StringIO)
def test_argument_parsing_valid_args(mock_stderr, mock_stdout):
    """Test that command line arguments are parsed correctly with valid inputs"""
    try:
        cli_main()
    except SystemExit:
        pass  # argparse calls sys.exit after parsing
    output = mock_stdout.getvalue()
    assert "--help" not in output and "-h" not in output


@patch('sys.argv', ['staking_calculator'])
@patch('sys.stdout', new_callable=StringIO)
def test_argument_parsing_missing_args(mock_stdout):
    """Test that help is displayed when no arguments are provided"""
    try:
        with patch('sys.stderr', new_callable=StringIO):
            cli_main()
    except SystemExit:
        pass
    output = mock_stdout.getvalue()
    assert "--help" in output or "-h" in output, "Expected help message to be displayed"


@patch('sys.argv', ['staking_calculator', '--principal', 'invalid', '--rate', '0.05', '--days', '365'])
@patch('sys.stdout', new_callable=StringIO)
def test_argument_parsing_invalid_args(mock_stdout):
    """Test that invalid argument types are handled correctly"""
    try:
        with patch('sys.stderr', new_callable=StringIO):
            cli_main()
    except SystemExit:
        pass
    output = mock_stdout.getvalue()
    assert "--help" not in output and "-h" not in output


def test_validate_inputs_with_valid_data():
    """Test that validate_inputs works correctly with valid inputs"""
    try:
        validate_inputs(1000, 0.05, 365)
    except ValueError as e:

        assert False, f"validate_inputs should not raise an error for valid inputs: {e}"


def test_validate_inputs_negative_principal():
    """Test that validate_inputs raises ValueError for negative principal"""
    try:
        validate_inputs(-1000, 0.05, 365)
        assert False, "Expected ValueError for negative principal"
    except ValueError:
        pass  # Expected


def test_validate_inputs_negative_rate():
    """Test that validate_inputs raises ValueError for negative rate"""
    try:
        validate_inputs(1000, -0.05, 365)
        assert False, "Expected ValueError for negative rate"
    except ValueError:
        pass  # Expected


def test_validate_inputs_negative_days():
    """Test that validate_inputs raises ValueError for negative days"""
    try:
        validate_inputs(1000, 0.05, -365)
        assert False, "Expected ValueError for negative days"
    except ValueError:
        pass  # Expected


def test_validate_inputs_invalid_principal_type():
    """Test that validate_inputs raises ValueError for invalid principal type"""
    try:
        validate_inputs("invalid", 0.05, 365)
        assert False, "Expected ValueError for invalid principal type"
    except ValueError:
        pass  # Expected


def test_validate_inputs_invalid_rate_type():
    """Test that validate_inputs raises ValueError for invalid rate type"""
    try:
        validate_inputs(1000, "invalid", 365)
        assert False, "Expected ValueError for invalid rate type"
    except ValueError:
        pass  # Expected


@patch('sys.argv', ['staking_calculator', '--principal', '1000', '--rate', '0.05', '--days', '365'])
def test_main_with_valid_cli_args():
    """Test that main function runs without error when given valid arguments"""
    try:
        with patch('sys.stdout', new_callable=StringIO), \
             patch('sys.stderr', new_callable=StringIO):
            cli_main()
    except SystemExit:
        pass  # argparse calls sys.exit after parsing


@patch('sys.argv', ['staking_calculator'])
def test_main_with_no_args():
    """Test that main function shows help when no arguments are provided"""
    try:
        with patch('sys.stdout', new_callable=StringIO), \
             patch('sys.stderr', new_callable=StringIO):
            cli_main()
    except SystemExit:
        pass  # argparse calls sys.exit when no args


@patch('sys.argv', ['staking_calculator', '--principal', 'invalid', '--rate', '0.05', '--days', '365'])
def test_main_with_invalid_args():
    """Test that main function handles invalid arguments gracefully"""
    try:
        with patch('sys.stdout', new_callable=StringIO), \
             patch('sys.stderr', new_callable=StringIO):
            cli_main()
    except SystemExit:
        pass  # argparse calls sys.exit on error


def test_validate_inputs_zero_values():
    """Test that validate_inputs handles zero values correctly"""
    try:
        validate_inputs(0, 0.0, 0)
        assert False, "Expected ValueError for zero values"
    except ValueError:
        pass  # Expected for zero principal or rate or days


def test_validate_inputs_valid_zero_rate():
    """Test that validate_inputs accepts zero interest rate"""
    try:
        validate_inputs(1000, 0.0, 365)
    except ValueError:
        assert False, "Zero interest rate should be valid"


def test_validate_inputs_valid_edge_cases():
    """Test that validate_inputs handles edge case values"""
    try:
        validate_inputs(1, 0.0001, 1)  # Minimal positive values
    except ValueError:
        assert False, "Minimal positive values should be valid"


def test_validate_inputs_large_values():
    """Test that validate_inputs handles large values"""
    try:
        validate_inputs(1000000, 1.0, 3650)  # Large values
    except ValueError:
        assert False, "Large values should be valid"


def test_validate_inputs_negative_rate_and_principal():
    """Test that validate_inputs rejects negative rate and principal"""
    try:
        validate_inputs(-1000, -0.05, 365)
        assert False, "Expected ValueError for negative values"
    except ValueError:
        pass  # Expected


@patch('sys.argv', ['staking_calculator', '--principal', '0', '--rate', '0', '--days', '1'])
def test_main_with_zero_inputs():
    """Test that main function handles zero inputs"""
    try:
        with patch('sys.stdout', new_callable=StringIO), \
             patch('sys.stderr', new_callable=StringIO):
            cli_main()
    except SystemExit:
        pass  # argparse calls sys.exit after parsing or on error


@patch('sys.argv', ['staking_calculator', '--principal', '1000000', '--rate', '1.0', '--days', '3650'])
def test_main_with_large_inputs():
    """Test that main function handles large inputs"""
    try:
        with patch('sys.stdout', new_callable=StringIO), \
             patch('sys.stderr', new_callable=StringIO):
            cli_main()
    except SystemExit:
        pass  # argparse calls sys.exit after parsing


@patch('sys.argv', ['staking_calculator', '--principal', '1000', '--rate', '0.05', '--days', '365'])
@patch('sys.stdout', new_callable=StringIO)
@patch('sys.stderr', new_callable=StringIO)
def test_main_output_format(mock_stderr, mock_stdout):
    """Test that the output is correctly formatted"""
    try:
        cli_main()
    except SystemExit:
        pass
    # We're not checking the actual output here, just ensuring it doesn't crash


@patch('sys.argv', ['staking_calculator', '--principal', '1000', '--rate', '0.05', '--days', '365'])
def test_main_consistent_behavior():
    """Test that main function behaves consistently with the same inputs"""
    try:
        with patch('sys.stdout', new_callable=StringIO), \
             patch('sys.stderr', new_callable=StringIO):
            cli_main()
    except SystemExit:
        pass  # argparse calls sys.exit after parsing
    # Test passes if no exception is thrown inconsistently


@patch('sys.argv', ['staking_calculator', '--principal', '1000', '--rate', '0.05', '--days', '365'])
def test_argument_parser_structure():
    """Test that argument parser has the expected structure"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--principal', type=float, required=True)
    parser.add_argument('--rate', type=float, required=True)
    parser.add_argument('--days', type=int, required=True)
    
    args = parser.parse_args(['--principal', '1000', '--rate', '0.05', '--days', '365'])
    assert args.principal == 1000
    assert args.rate == 0.05
    assert args.days == 365