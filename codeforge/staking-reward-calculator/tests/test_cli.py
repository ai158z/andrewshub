import argparse
from unittest.mock import patch, MagicMock
from src.cli import parse_args, run_calculations

def test_parse_args_principal_required():
    with patch('sys.argv', ['program', '--principal', '1000.0', '--apr', '0.05', '--duration', '365']):
        with patch('src.cli.to_float') as mock_to_float:
            mock_to_float.side_effect = [1000.0, 0.05]
            args = parse_args()
            assert args.principal == 1000.0
            assert args.apr == 0.05

def test_parse_args_compound_frequency_default():
    with patch('sys.argv', ['program', '--principal', '1000.0', '--apr', '0.05', '--duration', '365']):
        with patch('src.cli.to_int', return_value=365):
            args = parse_args()
            assert args.compound_frequency == 365

def test_parse_args_lockup_penalty_default():
    with patch('sys.argv', ['program', '--principal', '1000.0', '--apr', '0.05', '--duration', '365', '--lockup-penalty', '0.1']):
        with patch('src.cli.to_float', return_value=0.1):
            args = parse_args()
            assert args.lockup_penalty == 0.1

def test_run_calculations_validates_inputs():
    args = argparse.Namespace()
    args.principal = 1000.0
    args.apr = 0.05
    args.duration = 365
    args.compound_frequency = 365
    args.lockup_penalty = 0.0
    with patch('src.cli.validate_principal') as mock_validate_p:
        with patch('src.cli.validate_apr') as mock_validate_a:
            run_calculations(args)
            mock_validate_p.assert_called_once_with(args.principal)
            mock_validate_a.assert_called_once_with(args.apr)

def test_run_calculations_calculates_apy():
    args = argparse.Namespace()
    args.principal = 1000.0
    args.apr = 0.05
    args.duration = 365
    args.compound_frequency = 365
    args.lockup_penalty = 0.0
    with patch('src.cli.calculate_apy') as mock_calc_apy:
        mock_calc_apy.return_value = 0.0512
        apy = mock_calc_apy.return_value
        result = run_calculations(args)
        assert result['apy'] == apy

def test_run_calculations_compound_interest():
    args = argparse.Namespace()
    args.principal = 1000.0
    args.apr = 0.05
    args.duration = 365
    args.compound_frequency = 365
    args.lockup_penalty = 0.0
    with patch('src.cli.calculate_compound_interest') as mock_calc_compound:
        mock_calc_compound.return_value = 1051.27
        result = run_calculations(args)
        assert result['final_amount'] == 1051.27

def test_run_calculations_lockup_penalty():
    args = argparse.Namespace()
    args.principal = 1000.0
    args.apr = 0.05
    args.duration = 365
    args.compound_frequency = 365
    args.lockup_penalty = 0.1
    with patch('src.cli.calculate_lockup_penalty') as mock_calc_penalty:
        mock_calc_penalty.return_value = 50.0
        result = run_calculations(args)
        assert result['penalty'] == 50.0

def test_run_calculations_reward_calculation():
    args = argparse.Namespace()
    args.principal = 1000.0
    args.apr = 0.05
    args.duration = 365
    args.compound_frequency = 365
    args.lockup_penalty = 0.0
    result = run_calculations(args)
    assert 'reward' in result

def test_run_calculations_full_flow():
    args = argparse.Namespace()
    args.principal = 1000.0
    args.apr = 0.05
    args.duration = 365
    args.compound_frequency = 365
    args.lockup_penalty = 0.0
    with patch('src.cli.calculate_compound_interest', return_value=1051.27):
        with patch('src.cli.calculate_apy', return_value=0.0512):
            with patch('src.cli.calculate_lockup_penalty', return_value=50.0):
                result = run_calculations(args)
                assert result['reward'] == 1.27

def test_parse_args_missing_principal():
    try:
        parse_args()
    except SystemExit:
        pass

def test_parse_args_missing_apr():
    try:
        parse_args()
    except SystemExit:
        pass

def test_parse_args_missing_duration():
    try:
        parse_args()
    except SystemExit:
        pass

def test_parse_args_valid_compound_frequency():
    with patch('sys.argv', ['program', '--principal', '1000.0', '--apr', '0.05', '--duration', '365']):
        args = parse_args()
        assert args.compound_frequency == 365

def test_parse_args_valid_lockup_penalty():
    with patch('sys.argv', ['program', '--principal', '1000.0', '--apr', '0.05', '--duration', '365', '--lockup-penalty', '0.1']):
        args = parse_args()
        assert args.lockup_penalty == 0.1

def test_run_calculations_edge_case_zero_division():
    args = argparse.Namespace()
    args.principal = 0.0
    args.apr = 0.0
    args.duration = 0
    args.compound_frequency = 1
    args.lockup_penalty = 0.0
    result = run_calculations(args)
    assert result['apy'] == 0.0

def test_run_calculations_edge_case_no_compounding():
    args = argparse.Namespace()
    args.principal = 1000.0
    args.apr = 0.0
    args.duration = 0
    args.compound_frequency = 1
    args.lockup_penalty = 0.0
    result = run_calculations(args)
    assert result['apy'] == 0.0

def test_run_calculations_edge_case_high_compounding():
    args = argparse.Namespace()
    args.principal = 1000.0
    args.apr = 0.05
    args.duration = 10000
    args.compound_frequency = 10000
    args.lockup_penalty = 0.0
    with patch('src.cli.calculate_compound_interest', return_value=10000.0):
        result = run_calculations(args)
        assert result['final_amount'] == 10000.0

def test_run_calculations_edge_case_negative_penalty():
    args = argparse.Namespace()
    args.principal = -1000.0
    args.apr = -0.05
    args.duration = -365
    args.compound_frequency = -365
    args.lockup_penalty = -0.1
    result = run_calculations(args)
    assert result['penalty'] == 0.0

def test_run_calculations_edge_case_large_numbers():
    args = argparse.Namespace()
    args.principal = 1e10
    args.apr = 1e10
    args.duration = 365
    args.compound_frequency = 365
    args.lockup_penalty = 0.0
    result = run_calculations(args)
    assert result['reward'] == 1e10

def test_run_calculations_edge_case_zero_duration():
    args = argparse.Namespace()
    args.principal = 1000.0
    args.apr = 0.05
    args.duration = 0
    args.compound_frequency = 365
    args.lockup_penalty = 0.0
    result = run_calculations(args)
    assert result['reward'] == 0.0