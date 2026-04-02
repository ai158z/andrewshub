import pytest
from decimal import Decimal
from unittest.mock import patch, Mock
import sys
from io import StringIO

from src.cli import main

def test_main_no_arguments_shows_help():
    with patch('sys.argv', ['script.py']), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        with patch('argparse.ArgumentParser.print_help') as mock_print_help:
            main()
            mock_print_help.assert_called_once()

def test_main_valid_inputs_detailed_output():
    with patch('sys.argv', [
        'script.py', '--principal', '1000', '--rate', '0.05', 
        '--days', '365', '--compound-frequency', '1', 
        '--penalty-rate', '0.02', '--output-format', 'detailed'
    ]):
        result = main()
        assert result is not None

def test_main_valid_inputs_simple_output():
    with patch('sys.argv', [
        'script.py', '--principal', '1000', '--rate', '0.05', 
        '--days', '365', '--compound-frequency', '1', 
        '--penalty-rate', '0.02', '--output-format', 'simple'
    ]):
        result = main()
        assert result is not None

def test_main_invalid_principal():
    with patch('sys.argv', ['script.py', '--principal', '-100']), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        result = main()
        assert "Invalid input: Principal must be positive" in mock_stdout.getvalue()

def test_main_invalid_rate():
    with patch('sys.argv', ['script.py', '--rate', '-0.05']), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        result = main()
        assert "Invalid input: Rate must be between 0 and 1" in mock_stdout.getvalue()

def test_main_invalid_days():
    with patch('sys.argv', ['script.py', '--days', '-10']), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        result = main()
        assert "Invalid input: Days must be positive" in mock_stdout.getvalue()

def test_main_invalid_compound_frequency():
    with patch('sys.argv', ['script.py', '--compound-frequency', '0']), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        result = main()
        assert "Invalid input: Compound frequency must be positive" in mock_stdout.getvalue()

def test_main_invalid_penalty_rate():
    with patch('sys.argv', ['script.py', '--penalty-rate', '1.5']), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        result = main()
        assert "Invalid input: Penalty rate must be between 0 and 1" in mock_stdout.getvalue()

def test_main_default_values():
    with patch('sys.argv', ['script.py']), \
         patch('argparse.ArgumentParser.print_help') as mock_print_help:
        main()
        mock_print_help.assert_called_once()

def test_main_with_all_default_args():
    with patch('sys.argv', ['script.py', '--principal', '1000', '--rate', '0.05', '--days', '365']):
        result = main()
        assert result is not None

def test_main_custom_values():
    with patch('sys.argv', [
        'script.py', '--principal', '5000', '--rate', '0.12', 
        '--days', '180', '--compound-frequency', '4', 
        '--penalty-rate', '0.05'
    ]):
        result = main()
        assert result is not None

def test_main_zero_principal():
    with patch('sys.argv', ['script.py', '--principal', '0']), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        result = main()
        assert "Invalid input: Principal must be positive" in mock_stdout.getvalue()

def test_main_zero_rate():
    with patch('sys.argv', ['script.py', '--rate', '0']):
        result = main()
        assert result is not None

def test_main_zero_days():
    with patch('sys.argv', ['script.py', '--days', '0']), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        result = main()
        assert "Invalid input: Days must be positive" in mock_stdout.getvalue()

def test_main_large_compound_frequency():
    with patch('sys.argv', [
        'script.py', '--principal', '10000', '--rate', '0.15', 
        '--days', '730', '--compound-frequency', '365'
    ]):
        result = main()
        assert result is not None

def test_main_edge_case_zero_values():
    with patch('sys.argv', [
        'script.py', '--principal', '1', '--rate', '0', 
        '--days', '1', '--compound-frequency', '1'
    ]):
        result = main()
        assert result is not None

def test_main_edge_case_maximum_values():
    with patch('sys.argv', [
        'script.py', '--principal', '1000000', '--rate', '1.0', 
        '--days', '3650', '--compound-frequency', '365'
    ]):
        result = main()
        assert result is not None

def test_main_negative_compound_frequency():
    with patch('sys.argv', ['script.py', '--compound-frequency', '-1']), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        result = main()
        assert "Invalid input: Compound frequency must be positive" in mock_stdout.getvalue()