import pytest
from dyson_simulator.utils import format_output, parse_input
from dyson_simulator.models import SimulationParameters, SimulationResults
from unittest.mock import Mock
import json

# Test format_output with SimulationParameters in json format
def test_format_output_simulation_parameters_json():
    params = SimulationParameters(target_capture_percent=50.0, launch_mass_rate=1000.0)
    output = format_output(params, "json")
    # Parse the JSON to validate structure
    parsed = json.loads(output)
    assert "target capture percent" in parsed
    assert "launch mass rate" in parsed

# Test format_output with SimulationResults in json format
def test_format_output_simulation_results_json():
    params = SimulationParameters(target_capture_percent=30.0, launch_mass_rate=500.0)
    results = SimulationResults(
        target_capture_percent=params.target_capture_percent,
        required_mass=1e18,
        collector_area=2e10,
        timeline=100.0,
        parameters=params
    )
    output = format_output(results, "json")
    # Parse the JSON to validate structure
    parsed = json.loads(output)
    assert "parameters" in parsed

# Test format_output with invalid data type
def test_format_output_invalid_data_type():
    with pytest.raises(ValueError, match="Data must be SimulationParameters or SimulationResults instance"):
        format_output("invalid", "json")

# Test format_output with invalid format
def test_format_output_invalid_format():
    params = SimulationParameters(target_capture_percent=50.0, launch_mass_rate=1000.0)
    with pytest.raises(ValueError, match="Unsupported output format"):
        format_output(params, "invalid_format")

# Test format_output with text format for SimulationParameters
def test_format_output_simulation_parameters_text():
    params = SimulationParameters(target_capture_percent=50.0, launch_mass_rate=1000.0)
    output = format_output(params, "text")
    assert "Target: 50.0%" in output
    assert "Launch Mass Rate: 1000.0" in output

# Test format_output with detailed format for SimulationParameters
def test_format_output_simulation_parameters_detailed():
    params = SimulationParameters(target_capture_percent=75.0, launch_mass_rate=1500.0)
    output = format_output(params, "detailed")
    assert "Simulation Parameters:" in output
    assert "Target Capture Percent: 75.0%" in output
    assert "Launch Mass Rate: 1500.0" in output

# Test format_output with text format for SimulationResults
def test_format_output_simulation_results_text():
    params = SimulationParameters(target_capture_percent=60.0, launch_mass_rate=1200.0)
    results = SimulationResults(
        target_capture_percent=params.target_capture_percent,
        required_mass=1e18,
        collector_area=2e10,
        timeline=100.0,
        parameters=params
    )
    output = format_output(results, "text")
    assert "Target: 60.0%" in output

# Test format_output with detailed format for SimulationResults
def test_format_output_simulation_results_detailed():
    params = SimulationParameters(target_capture_percent=40.0, launch_mass_rate=800.0)
    results = SimulationResults(
        target_capture_percent=params.target_capture_percent,
        required_mass=1e19,
        collector_area=1.5e11,
        timeline=200.0,
        parameters=params
    )
    output = format_output(results, "detailed")
    assert "Simulation Results:" in output
    assert "Target Capture Percent: 40.0%" in output
    assert "Required Mass: 1e+19" in output

# Test parse_input with valid JSON input
def test_parse_input_valid_json():
    input_json = '{"target_capture_percent": 75.0, "launch_mass_rate": 1000.0}'
    result = parse_input(input_json, "json")
    assert result.target_capture_percent == 75.0
    assert result.launch_mass_rate == 1000.0

# Test parse_input with valid CLI input
def test_parse_input_valid_cli():
    result = parse_input("75.0,1000.0", "cli")
    assert result.target_capture_percent == 75.0
    assert result.launch_mass_rate == 1000.0

# Test parse_input with invalid input type
def test_parse_input_invalid_input_type():
    with pytest.raises(ValueError, match="Input data must be a string"):
        parse_input(123, "json")

# Test parse_input with invalid format
def test_parse_input_invalid_format():
    with pytest.raises(ValueError, match="Input format must be 'json' or 'cli'"):
        parse_input("75.0,1000.0", "invalid")

# Test parse_input with invalid JSON input
def test_parse_input_invalid_json():
    with pytest.raises(ValueError, match="Invalid JSON input"):
        parse_input("invalid json", "json")

# Test parse_input with missing fields in JSON
def test_parse_input_missing_fields():
    with pytest.raises(ValueError, match="Missing required field"):
        parse_input('{"target_capture_percent": 75.0}', "json")

# Test parse_input with invalid CLI format
def test_parse_input_invalid_cli():
    with pytest.raises(ValueError, match="Invalid CLI input format"):
        parse_input("75.0,1000.0,500.0", "cli")

# Test parse_input with valid values
def test_parse_input_valid_values():
    input_data = '{"target_capture_percent": 75.0, "launch_mass_rate": 1000.0}'
    result = parse_input(input_data, "json")
    assert result.target_capture_percent == 75.0
    assert result.launch_mass_rate == 1000.0

# Test format_output with valid SimulationParameters
def test_format_output_valid_simulation_parameters():
    params = SimulationParameters(target_capture_percent=80.0, launch_mass_rate=1200.0)
    output = format_output(params, "json")
    parsed = json.loads(output)
    assert "target capture percent" in parsed
    assert "launch mass rate" in parsed

# Test format_output with valid SimulationResults
def test_format_output_valid_simulation_results():
    params = SimulationParameters(target_capture_percent=85.0, launch_mass_rate=1100.0)
    results = SimulationResults(
        target_capture_percent=params.target_capture_percent,
        required_mass=2e10,
        collector_area=1.5e10,
        timeline=150.0,
        parameters=params
    )
    output = format_output(results, "json")
    parsed = json.loads(output)
    assert "target capture percent" in parsed
    assert "required mass" in parsed

# Test format_output with invalid data type
def test_format_output_invalid_data():
    with pytest.raises(ValueError, match="Data must be SimulationParameters or SimulationResults instance"):
        format_output("invalid", "json")

# Test format_output with invalid format
def test_format_output_invalid_format():
    with pytest.raises(ValueError, match="Unsupported output format"):
        format_output(SimulationParameters(50.0, 1000.0), "invalid")

# Test edge case with 0% target capture
def test_parse_input_zero_capture():
    input_data = '{"target_capture_percent": 0, "launch_mass_rate": 1000.0}'
    result = parse_input(input_data, "json")
    assert result.target_capture_percent == 0
    assert result.launch_mass_rate == 1000.0

# Test edge case with 100% target capture
def test_parse_input_100_percent_capture():
    input_data = '{"target_capture_percent": 100, "launch_mass_rate": 1000.0}'
    result = parse_input(input_data, "json")
    assert result.target_capture_percent == 100
    assert result.launch_mass_rate == 1000.0

# Test edge case with negative mass rate
def test_parse_input_negative_mass_rate():
    input_data = '{"target_capture_percent": 75.0, "launch_mass_rate": -1000.0}'
    with pytest.raises(ValueError, match="Launch mass rate must be positive"):
        parse_input(input_data, "json")

# Test edge case with target capture out of range
def test_parse_input_target_capture_out_of_range():
    input_data = '{"target_capture_percent": 101, "launch_mass_rate": 1000.0}'
    with pytest.raises(ValueError, match="Target capture percent must be between 0 and 100"):
        parse_input(input_data, "json")

# Test format_output with empty input
def test_format_output_empty_input():
    with pytest.raises(ValueError, match="Data must be SimulationParameters or SimulationResults instance"):
        format_output("", "json")

# Test format_output with SimulationParameters
def test_format_output_simulation_parameters():
    params = SimulationParameters(target_capture_percent=75.0, launch_mass_rate=1000.0)
    output = format_output(params, "json")
    parsed = json.loads(output)
    assert parsed is not None

# Test format_output with SimulationResults
def test_format_output_simulation_results():
    params = SimulationParameters(target_capture_percent=80.0, launch_mass_rate=1200.0)
    results = SimulationResults(
        target_capture = 80.0,
        required_mass = 2e10,
        collector_area = 1.5e10,
        timeline = 100.0,
        parameters = params
    )
    output = format_output(results, "json")
    parsed = json.loads(output)
    assert parsed is not None

# Test format_output with detailed format
def test_format_output_detailed():
    params = SimulationParameters(target_capture_percent=75.0, launch_mass_rate=1000.0)
    output = format_output(params, "detailed")
    assert "Simulation Parameters:" in output
    assert "Target Capture Percent: 75.0%" in output
    assert "Launch Mass Rate: 1000.0" in output

# Test format_output with text format
def test_format_output_text():
    params = SimulationParameters(target_capture_percent=60.0, launch_mass_rate=800.0)
    output = format_output(params, "text")
    assert "Target: 60.0%" in output
    assert "Launch Mass Rate: 800.0" in output

# Test parse_input with valid CLI input
def test_parse_input_valid_cli():
    result = parse_input("75.0,1000.0", "cli")
    assert result.target_capture_percent == 75.0
    assert result.launch_mass_rate == 1000.0

# Test parse_input with invalid CLI input
def test_parse_input_invalid_cli():
    with pytest.raises(ValueError, match="Invalid CLI input format"):
        parse_input("75.0,1000.0,500.0", "cli")

# Test parse_input with valid JSON input
def test_parse_input_valid_json():
    input_data = '{"target_capture_percent": 75, "launch_mass_rate": 1000.0}'
    result = parse_input(input_data, "json")
    assert result.target_capture_percent == 75
    assert result.launch_mass_rate == 1000.0