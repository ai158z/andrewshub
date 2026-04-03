import pytest
from unittest.mock import patch, MagicMock
import argparse
import sys
from io import StringIO

from src.cli import parse_args, run_calculations
from src.staking_calculator import calculate_apy, calculate_compound_interest
from src.validator import validate_principal, validate_apr
from src.types import to_float, to_int


def test_parse_args_valid():
    test_args = [
        'staking-reward-calculator',
        '--principal', '1000',
        '--apr', '0.05',
        '--time', '365'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.principal == '1000'
        assert args.apr == '0.05'
        assert args.time == '365'


def test_parse_args_help(capsys):
    with patch('sys.argv', ['staking-reward-calculator', '--help']), \
         pytest.raises(SystemExit) as exc_info:
        parse_args()
    
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert 'usage:' in captured.out


def test_parse_args_version(capsys):
    with patch('sys.argv', ['staking-reward-calculator', '--version']), \
         pytest.raises(SystemExit) as exc_info:
        parse_args()
    
    assert exc_info.value.code == 0


def test_parse_args_invalid():
    with patch('sys.argv', ['staking-reward-calculator', '--invalid']), \
         pytest.raises(SystemExit) as exc_info:
        parse_args()
    
    assert exc_info.value.code == 2


def test_validate_principal_valid():
    assert validate_principal("1000") is True
    assert validate_principal("0.01") is True


def test_validate_principal_invalid():
    with pytest.raises(ValueError):
        validate_principal("invalid")
    
    with pytest.raises(ValueError):
        validate_principal("-100")


def test_validate_apr_valid():
    assert validate_apr("0.05") is True
    assert validate_apr("0.0001") is True


def test_validate_apr_invalid():
    with pytest.raises(ValueError):
        validate_apr("invalid")
    
    with pytest.raises(ValueError):
        validate_apr("1.5")


def test_calculate_compound_interest():
    principal = 1000
    rate = 0.05
    time = 1
    compound_frequency = 365
    
    result = calculate_compound_interest(principal, rate, time, compound_frequency)
    expected = principal * (1 + rate / compound_frequency) ** (compound_frequency * time)
    
    assert abs(result - expected) < 1e-10


def test_calculate_apy():
    rate = 0.05
    compound_frequency = 365
    
    apy = calculate_apy(rate, compound_frequency)
    expected_apy = (1 + rate) ** compound_frequency - 1
    
    assert abs(apy - expected_apy) < 1e-10


def test_to_float():
    assert to_float("0.05") == 0.05
    assert to_float("1000") == 1000.0
    
    with pytest.raises(ValueError):
        to_float("invalid")


def test_to_int():
    assert to_int("365") == 365
    assert to_int("1") == 1
    
    with pytest.raises(ValueError):
        to_int("invalid")


def test_run_calculations_basic(capsys):
    args = argparse.Namespace(principal='1000', apr='0.05', time='365')
    run_calculations(args)
    
    captured = capsys.readouterr()
    assert "Principal: 1000" in captured.out
    assert "APR: 5.0%" in captured.out


def test_run_calculations_edge_case(capsys):
    args = argparse.Namespace(principal='0.01', apr='0.0001', time='1')
    run_calculations(args)
    
    captured = capsys.readouterr()
    assert "Principal: 0.01" in captured.out


@patch('sys.stdout', new_callable=StringIO)
def test_full_cli_workflow(mock_stdout):
    test_args = [
        'staking-reward-calculator',
        '--principal', '1000',
        '--apr', '0.05',
        '--time', '365'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        run_calculations(args)
        
        output = mock_stdout.getvalue()
        assert "Principal: 1000" in output
        assert "APR: 5.0%" in output


def test_consistency_check():
    # Test that the same input always produces the same output
    principal = 1000
    rate = 0.05
    time = 1
    compound_frequency = 365
    
    result1 = calculate_compound_interest(principal, rate, time, compound_frequency)
    result2 = calculate_compound_interest(principal, rate, time, compound_frequency)
    
    assert result1 == result2


def test_output_formatting(capsys):
    args = argparse.Namespace(principal='1000', apr='0.05', time='365')
    run_calculations(args)
    
    captured = capsys.readouterr()
    output_lines = captured.out.strip().split('\n')
    
    assert len(output_lines) >= 3  # At least 3 lines of output
    assert any("Reward:" in line for line in output_lines)
    assert any("APY:" in line for line in output_lines)


def test_help_output_content(capsys):
    with patch('sys.argv', ['staking-reward-calculator', '--help']), \
         pytest.raises(SystemExit):
        parse_args()
    
    captured = capsys.readouterr()
    assert '--principal' in captured.out
    assert '--apr' in captured.out
    assert '--time' in captured.out


def test_version_output_content(capsys):
    with patch('sys.argv', ['staking-reward-calculator', '--version']), \
         pytest.raises(SystemExit):
        parse_args()
    
    captured = capsys.readouterr()
    assert 'staking-reward-calculator' in captured.out.lower()


def test_compound_interest_edge_cases():
    # Test with zero values
    assert calculate_compound_interest(0, 0.05, 1, 365) == 0
    assert calculate_compound_interest(1000, 0, 1, 365) == 1000
    
    # Test with extreme values
    result = calculate_compound_interest(1000, 0.0001, 1, 1)
    assert result > 1000  # Should be slightly more than principal due to compounding