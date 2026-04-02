import argparse
import pytest
from unittest.mock import patch, MagicMock
from src.main import main

def test_main_success():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=1000,
            duration=365,
            annual_rate=0.05,
            penalty_rate=0.01
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            with patch('src.main.print') as mock_print:
                result = main()
                assert result == 0

def test_main_exception_handling():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.side_effect = Exception("Test exception")
        with patch('src.main.print') as mock_print:
            result = main()
            assert result == 1

def test_main_keyboard_interrupt():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.side_effect = KeyboardInterrupt()
        result = main()
        assert result == 130

def test_main_with_args():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=1000,
            duration=365,
            annual_rate=0.05,
            penalty_rate=0.01
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            with patch('src.main.print') as mock_print:
                result = main()
                assert result == 0

def test_main_with_negative_stake():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=-1000,
            duration=365,
            annual_rate=0.05,
            penalty_rate=0.01
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 1
            result = main()
            assert result == 1

def test_main_with_zero_values():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=0,
            duration=0,
            annual_rate=0,
            penalty_rate=0
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            result = main()
            assert result == 0

def test_main_with_high_values():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=1000000,
            duration=36500,
            annual_rate=0.25,
            penalty_rate=0.1
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            result = main()
            assert result == 0

def test_main_with_decimal_precision():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=1000.999,
            duration=365.5,
            annual_rate=0.05123,
            penalty_rate=0.01456
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            result = main()
            assert result == 0

def test_main_with_maximum_values():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=999999999999999999999,
            duration=999999999999999999999,
            annual_rate=0.999999999999999999999,
            penalty_rate=0.999999999999999999999
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            result = main()
            assert result == 0

def test_main_with_minimum_values():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=0.000001,
            duration=1,
            annual_rate=0.000001,
            penalty_rate=0.000001
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            result = main()
            assert result == 0

def test_main_with_null_values():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=None,
            duration=None,
            annual_rate=None,
            penalty_rate=None
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 1
            result = main()
            assert result == 1

def test_main_with_string_values():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount="invalid",
            duration="invalid",
            annual_rate="invalid",
            penalty_rate="invalid"
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 1
            result = main()
            assert result == 1

def test_main_with_very_large_values():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=9999999999999999999999999999999999999999,
            duration=9999999999999999999999999999999999999999,
            annual_rate=0.9999999999999999999999999999999999999999,
            penalty_rate=0.9999999999999999999999999999999999999999
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            result = main()
            assert result == 0

def test_main_with_zero_stake_and_rate():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=0,
            duration=0,
            annual_rate=0,
            penalty_rate=0
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            result = main()
            assert result == 0

def test_main_with_negative_duration():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=1000,
            duration=-365,
            annual_rate=0.05,
            penalty_rate=0.01
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 1
            result = main()
            assert result == 1

def test_main_with_zero_duration():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=1000,
            duration=0,
            annual_rate=0.05,
            penalty_rate=0.01
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 1
            result = main()
            assert result == 1

def test_main_with_extreme_rates():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=1000,
            duration=365,
            annual_rate=999.999,
            penalty_rate=999.999
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            result = main()
            assert result == 0

def test_main_with_fractional_values():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=1000.5,
            duration=365.5,
            annual_rate=0.055,
            penalty_rate=0.015
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            result = main()
            assert result == 0

def test_main_with_large_stake():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=9999999999999999999999999999999999999999,
            duration=365,
            annual_rate=0.05,
            penalty_rate=0.01
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            result = main()
            assert result == 0

def test_main_with_very_small_penalty():
    with patch('src.main.parse_args') as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            stake_amount=1000,
            duration=365,
            annual_rate=0.05,
            penalty_rate=0.0000001
        )
        with patch('src.main.run_calculator') as mock_run:
            mock_run.return_value = 0
            result = main()
            assert result == 0