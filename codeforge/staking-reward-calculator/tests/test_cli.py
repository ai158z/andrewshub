import pytest
from unittest.mock import patch, MagicMock
from src.cli import validate_inputs, format_rewards_output, main
from click.testing import CliRunner

@pytest.fixture
def mock_dependencies():
    with patch('src.cli.get_network_apy') as mock_apy, \
         patch('src.cli.get_network_commission') as mock_commission, \
         patch('src.cli.calculate_rewards') as mock_calculate, \
         patch('src.cli.convert_to_fiat') as mock_convert, \
         patch('src.cli.analyze_network_risks') as mock_risks, \
         patch('src.cli.plot_rewards_over_time') as mock_plot:
        yield {
            'apy': mock_apy,
            'commission': mock_commission,
            'calculate': mock_calculate,
            'convert': mock_convert,
            'risks': mock_risks,
            'plot': mock_plot
        }

def test_validate_inputs_valid():
    # Should not raise any exception
    validate_inputs(100.0, 30, "ethereum", "USD")

def test_validate_inputs_invalid_stake_amount():
    with pytest.raises(ValueError, match="Stake amount must be positive"):
        validate_inputs(-50.0, 30, "ethereum", "USD")

def test_validate_inputs_zero_stake_amount():
    with pytest.raises(ValueError, match="Stake amount must be positive"):
        validate_inputs(0, 30, "ethereum", "USD")

def test_validate_inputs_invalid_duration():
    with pytest.raises(ValueError, match="Duration must be positive"):
        validate_inputs(100.0, -5, "ethereum", "USD")

def test_validate_inputs_zero_duration():
    with pytest.raises(ValueError, match="Duration must be positive"):
        validate_inputs(100.0, 0, "ethereum", "USD")

def test_validate_inputs_empty_network():
    with pytest.raises(ValueError, match="Network cannot be empty"):
        validate_inputs(100.0, 30, "", "USD")

def test_validate_inputs_empty_currency():
    with pytest.raises(ValueError, match="Currency cannot be empty"):
        validate_inputs(100.0, 30, "ethereum", "")

def test_format_rewards_output():
    rewards_data = {
        'initial_stake': 100.0,
        'final_value': 150.543210,
        'total_rewards': 50.123456,
        'roi': 50.12
    }
    output = format_rewards_output(rewards_data)
    expected = """Staking Rewards Summary:
  Initial Stake: 100.0 tokens
  Final Value: 150.543210 tokens
  Total Rewards: 50.123456 tokens
  ROI: 50.12%"""
    assert output == expected

def test_main_success(mock_dependencies):
    # Setup mocks
    mock_dependencies['apy'].return_value = 0.12
    mock_dependencies['commission'].return_value = 0.05
    mock_dependencies['calculate'].return_value = {
        'initial_stake': 100.0,
        'final_value': 150.543210,
        'total_rewards': 50.123456,
        'roi': 50.12
    }
    mock_dependencies['convert'].side_effect = lambda amount, network, currency: amount * 2  # Simple mock conversion
    mock_dependencies['risks'].return_value = {'slashing': 'medium', 'impermanent_loss': 'low'}
    mock_dependencies['plot'].return_value = MagicMock()
    
    runner = CliRunner()
    with patch('src.cli.click.echo') as mock_echo:
        result = runner.invoke(main, ['--stake-amount', '100', '--duration', '30', '--network', 'ethereum', '--currency', 'USD'])
        assert result.exit_code == 0

def test_main_invalid_inputs():
    runner = CliRunner()
    result = runner.invoke(main, ['--stake-amount', '-50', '--duration', '30', '--network', 'ethereum'])
    assert result.exit_code == 1
    assert "Invalid input" in result.output

def test_main_network_apy_exception():
    with patch('src.cli.get_network_apy', side_effect=Exception("Network not found")):
        runner = CliRunner()
        result = runner.invoke(main, ['--stake-amount', '100', '--duration', '30', '--network', 'invalid_network'])
        assert result.exit_code == 1
        assert "An error occurred" in result.output

def test_main_calculation_exception():
    with patch('src.cli.get_network_apy', return_value=0.12), \
         patch('src.cli.get_network_commission', return_value=0.05), \
         patch('src.cli.calculate_rewards', side_effect=Exception("Calculation error")):
        runner = CliRunner()
        result = runner.invoke(main, ['--stake-amount', '100', '--duration', '30', '--network', 'ethereum'])
        assert result.exit_code == 1
        assert "An error occurred" in result.output

def test_main_with_defaults():
    with patch('src.cli.get_network_apy', return_value=0.12), \
         patch('src.cli.get_network_commission', return_value=0.05), \
         patch('src.cli.calculate_rewards') as mock_calc, \
         patch('src.cli.convert_to_fiat', side_effect=lambda x, y, z: x * 2), \
         patch('src.cli.analyze_network_risks', return_value={'risk': 'low'}), \
         patch('src.cli.plot_rewards_over_time', return_value=MagicMock()):
        
        mock_calc.return_value = {
            'initial_stake': 100.0,
            'final_value': 150.543210,
            'total_rewards': 50.123456,
            'roi': 50.12
        }
        
        runner = CliRunner()
        result = runner.invoke(main, ['--stake-amount', '100', '--duration', '30', '--network', 'ethereum'])
        assert result.exit_code == 0
        assert "Staking Rewards Summary" in result.output

def test_main_default_currency():
    with patch('src.cli.get_network_apy', return_value=0.12), \
         patch('src.cli.get_network_commission', return_value=0.05), \
         patch('src.cli.calculate_rewards') as mock_calc, \
         patch('src.cli.convert_to_fiat', side_effect=lambda x, y, z: x * 2), \
         patch('src.cli.analyze_network_risks', return_value={'risk': 'low'}), \
         patch('src.cli.plot_rewards_over_time', return_value=MagicMock()):

        mock_calc.return_value = {
            'initial_stake': 100.0,
            'final_value': 150.543210,
            'total_rewards': 50.123456,
            'roi': 50.12
        }
        
        runner = CliRunner()
        result = runner.invoke(main, [
            '--stake-amount', '100', 
            '--duration', '30', 
            '--network', 'ethereum',
            '--currency', 'USD'
        ])
        assert result.exit_code == 0