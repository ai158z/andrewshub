import argparse
import logging
import pytest
from unittest.mock import patch, MagicMock
from src.cli import parse_args, run_calculator, main

def test_parse_args_valid_inputs():
    test_args = [
        "--stake_amount", "1000.0",
        "--duration", "365"
    ]
    with patch("sys.argv", ["cli.py"] + test_args):
        args = parse_args()
        assert args.stake_amount == 1000.0
        assert args.duration == 365
        assert args.lockup_percent == 0.0
        assert args.annual_rate == 0.08
        assert args.penalty_rate == 0.02

def test_parse_args_missing_required_args():
    test_args = ["--stake_amount", "1000.0"]
    with patch("sys.argv", ["cli.py"] + test_args):
        with pytest.raises(SystemExit):
            parse_args()

def test_parse_args_with_optional_args():
    test_args = [
        "--stake_amount", "1000.0",
        "--duration", "365",
        "--lockup_percent", "10.0",
        "--annual_rate", "0.1",
        "--penalty_rate", "0.05"
    ]
    with patch("sys.argv", ["cli.py"] + test_args):
        args = parse_args()
        assert args.lockup_percent == 10.0
        assert args.annual_rate == 0.1
        assert args.penalty_rate == 0.05

@patch("src.cli.calculate_staking_reward")
def test_run_calculator_valid_inputs(mock_calculate):
    mock_calculate.return_value = 80.0
    with patch("builtins.print") as mock_print:
        run_calculator(1000.0, 365, 0.0)
        mock_calculate.assert_called_once_with(1000.0, 365, 0.08, 0.02)
        mock_print.assert_called_with("Estimated Reward: $80.00")

def test_run_calculator_negative_stake_amount():
    with patch("builtins.print") as mock_print:
        run_calculator(-1000.0, 365, 0.0)
        mock_print.assert_called_with("Error calculating reward: Stake amount must be positive")

def test_run_calculator_zero_duration():
    with patch("builtins.print") as mock_print:
        run_calculator(1000.0, 0, 0.0)
        mock_print.assert_called_with("Error calculating reward: Duration must be positive")

def test_run_calculator_invalid_lockup_percent():
    with patch("builtins.print") as mock_print:
        run_calculator(1000.0, 365, 150.0)
        mock_print.assert_called_with("Error calculating reward: Lockup percent must be between 0 and 100")

@patch("src.cli.calculate_staking_reward")
def test_run_calculator_exception_handling(mock_calculate):
    mock_calculate.side_effect = Exception("Calculation failed")
    with patch("builtins.print") as mock_print:
        run_calculator(1000.0, 365, 0.0)
        mock_print.assert_called_with("Error calculating reward: Calculation failed")

@patch("src.cli.parse_args")
def test_main_success_path(mock_parse):
    mock_parse.return_value = argparse.Namespace(
        stake_amount=1000.0,
        duration=365,
        lockup_percent=0.0
    )
    with patch("src.cli.run_calculator") as mock_run:
        with patch("sys.exit") as mock_exit:
            main()
            mock_run.assert_called_once_with(1000.0, 365, 0.0)
            mock_exit.assert_called_once_with(0)

@patch("src.cli.parse_args")
def test_main_exception_handling(mock_parse):
    mock_parse.side_effect = Exception("Parsing failed")
    with patch("builtins.print") as mock_print:
        with patch("sys.exit") as mock_exit:
            main()
            mock_print.assert_called_with("Application error: Parsing failed")
            mock_exit.assert_called_once_with(1)

def test_main_integration():
    test_args = [
        "cli.py",
        "--stake_amount", "1000.0",
        "--duration", "365"
    ]
    with patch("sys.argv", test_args):
        with patch("src.cli.run_calculator") as mock_run:
            with patch("sys.exit") as mock_exit:
                main()
                mock_run.assert_called_once_with(1000.0, 365, 0.0)
                mock_exit.assert_called_once_with(0)