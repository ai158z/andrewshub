import pytest
from click.testing import CliRunner
from unittest.mock import patch, mock_open
from dyson_simulator.cli import cli
from dyson_simulator.models import SimulationParameters
from dyson_simulator.main import SimulationResults

def test_cli_group_exists():
    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0

def test_simulate_command_exists():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert 'simulate' in result.output

def test_simulate_missing_required_options():
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate'])
    assert result.exit_code != 0
    assert 'Missing option' in result.output

def test_simulate_invalid_target_capture_negative():
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '-10', '--launch-mass-rate', '1000'])
    assert result.exit_code == 2
    assert 'Target capture must be between 0 and 100 percent' in result.output

def test_simulate_invalid_target_capture_over_100():
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '110', '--launch-mass-rate', '1000'])
    assert result.exit_code == 2

def test_simulate_invalid_launch_mass_rate():
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '50', '--launch-mass-rate', '-100'])
    assert result.exit_code == 2
    assert 'Launch mass rate must be positive' in result.output

@patch('dyson_simulator.cli.run_simulation')
def test_simulate_valid_input(mock_run_simulation):
    mock_run_simulation.return_value = SimulationResults(
        timeline_years=50,
        total_mass_required=1000000,
        collector_area_m2=50000
    )
    
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '75', '--launch-mass-rate', '1000'])
    assert result.exit_code == 0
    assert 'Simulation Results' in result.output

@patch('dyson_simulator.cli.run_simulation')
def test_simulate_with_output_file(mock_run_simulation):
    mock_run_simulation.return_value = SimulationResults(
        timeline_years=30,
        total_mass_required=500000,
        collector_area_m2=25000
    )
    
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            'simulate', 
            '--target-capture', '50', 
            '--launch-mass-rate', '2000',
            '--output-file', 'results.txt'
        ])
        assert result.exit_code == 0
        # Verify file was written
        with open('results.txt') as f:
            content = f.read()
            assert 'Simulation Results' in content

@patch('dyson_simulator.cli.run_simulation')
def test_simulate_parameters_passed_correctly(mock_run_simulation):
    mock_run_simulation.return_value = SimulationResults(
        timeline_years=40,
        total_mass_required=750000,
        collector_area_m2=30000
    )
    
    runner = CliRunner()
    result = runner.invoke(cli, [
        'simulate', 
        '--target-capture', '60', 
        '--launch-mass-rate', '1500'
    ])
    
    assert result.exit_code == 0
    mock_run_simulation.assert_called_once()
    args = mock_run_simulation.call_args[0][0]
    assert isinstance(args, SimulationParameters)
    assert args.target_capture_percent == 60
    assert args.launch_mass_rate == 1500

def test_simulate_command_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--help'])
    assert result.exit_code == 0
    assert 'Run a Dyson swarm simulation' in result.output

@patch('dyson_simulator.cli.run_simulation')
def test_simulate_output_format(mock_run_simulation):
    mock_run_simulation.return_value = SimulationResults(
        timeline_years=45,
        total_mass_required=800000,
        collector_area_m2=40000
    )
    
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '80', '--launch-mass-rate', '3000'])
    assert result.exit_code == 0
    assert 'Simulation Results for 80.0% capture target:' in result.output
    assert 'Timeline: 45 years' in result.output
    assert 'Required Mass: 800000 kg' in result.output
    assert 'Collector Area: 40000 m²' in result.output

@patch('dyson_simulator.cli.run_simulation')
def test_simulation_error_handling(mock_run_simulation):
    mock_run_simulation.side_effect = Exception("Simulation error")
    
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '50', '--launch-mass-rate', '1000'])
    assert result.exit_code == 1
    assert 'Simulation failed' in result.output

def test_invalid_option_combinations():
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '50'])
    assert result.exit_code != 0
    assert 'Missing option' in result.output

@patch('dyson_simulator.cli.run_simulation')
def test_edge_case_zero_capture(mock_run_simulation):
    mock_run_simulation.return_value = SimulationResults(
        timeline_years=0,
        total_mass_required=0,
        collector_area_m2=0
    )
    
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '0', '--launch-mass-rate', '1000'])
    assert result.exit_code == 0

@patch('dyson_simulator.cli.run_simulation')
def test_edge_case_100_percent_capture(mock_run_simulation):
    mock_run_simulation.return_value = SimulationResults(
        timeline_years=1000,
        total_mass_required=999999999,
        collector_area_m2=999999999
    )
    
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '100', '--launch-mass-rate', '5000'])
    assert 'Simulation Results' in result.output

def test_invalid_option_types():
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', 'invalid', '--launch-mass-rate', '1000'])
    assert result.exit_code == 2

def test_missing_launch_mass_rate():
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '50'])
    assert result.exit_code != 0

@patch('dyson_simulator.cli.run_simulation')
def test_valid_float_inputs(mock_run_simulation):
    mock_run_simulation.return_value = SimulationResults(
        timeline_years=25,
        total_mass_required=100000,
        collector_area_m2=10000
    )
    
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '75.5', '--launch-mass-rate', '1500.5'])
    assert result.exit_code == 0

@patch('dyson_simulator.cli.run_simulation')
def test_simulation_parameters_structure(mock_run_simulation):
    mock_run_simulation.return_value = SimulationResults(
        timeline_years=35,
        total_mass_required=500000,
        collector_area_m2=25000
    )
    
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '65', '--launch-mass-rate', '2000'])
    assert result.exit_code == 0
    mock_run_simulation.assert_called_once()

@patch('dyson_simulator.cli.run_simulation')
def test_file_output_functionality(mock_run_simulation):
    mock_run_simulation.return_value = SimulationResults(
        timeline_years=20,
        total_mass_required=300000,
        collector_area_m2=15000
    )
    
    with patch('builtins.open', mock_open()) as mocked_file:
        runner = CliRunner()
        result = runner.invoke(cli, [
            'simulate', 
            '--target-capture', '45', 
            '--launch-mass-rate', '2500',
            '--output-file', 'test_output.txt'
        ])
        assert result.exit_code == 0
        mocked_file.assert_called_once_with('test_output.txt', 'w')

@patch('dyson_simulator.cli.run_simulation')
def test_simulation_failure(mock_run_simulation):
    mock_run_simulation.side_effect = ValueError("Test error")
    
    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', '--target-capture', '50', '--launch-mass-rate', '1000'])
    assert result.exit_code == 1
    assert 'Simulation failed' in result.output