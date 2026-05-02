import json
import sys
from typing import Any, Dict, Union
from dyson_simulator.models import SimulationParameters, SimulationResults

def format_output(data: Union[SimulationParameters, SimulationResults], output_format: str = "json") -> str:
    """Format simulation data for output.
    
    Args:
        data: Either SimulationParameters or SimulationResults instance
        output_format: Output format - 'json', 'text', or 'detailed'
        
    Returns:
        Formatted string representation of the data
        
    Raises:
        ValueError: If data is not a valid type or format is unsupported
    """
    if not isinstance(data, (SimulationParameters, SimulationResults)):
        raise ValueError("Data must be SimulationParameters or SimulationResults instance")
    
    if output_format not in ["json", "text", "detailed"]:
        raise ValueError("Unsupported output format. Use 'json', 'text', or 'detailed'")
    
    if output_format == "json":
        if isinstance(data, SimulationParameters):
            result = {
                "target capture percent": data.target_capture_percent,
                "launch mass rate": data.launch_mass_rate
            }
        else:  # SimulationResults
            result = {
                "target capture percent": data.target_capture_percent,
                "required mass": data.required_mass,
                "collector area": data.collector_area,
                "timeline": data.timeline,
                "parameters": {
                    "target capture percent": data.parameters.target_capture_percent if data.parameters else None,
                    "launch mass rate": data.parameters.launch_mass_rate if data.parameters else None
                }
            }
        return json.dumps(result, indent=2)
    
    elif output_format == "text":
        if isinstance(data, SimulationParameters):
            return f"Target: {data.target_capture_percent}% Dyson capture"
        else:  # SimulationResults
            return (f"Target: {data.target_capture_percent}%\n"
                   f"Required mass: {data.required_mass:.2e} kg\n"
                   f"Collector area: {data.collector_area:.2e} m²\n"
                   f"Timeline: {data.timeline:.2f} years")
    
    else:  # detailed
        if isinstance(data, SimulationParameters):
            return (f"Simulation Parameters:\n"
                   f"  Target Capture Percent: {data.target_capture_percent}%\n"
                   f"  Launch Mass Rate: {data.launch_mass_rate} kg/year\n"
                   f"  Solar Luminosity: {SOLAR_LUMINOSITY} W\n"
                   f"  Capture Efficiency: {DYSON_CAPTURE_EFFICIENCY * 100}%")
        else:  # SimulationResults
            return (f"Simulation Results:\n"
                   f"  Target Capture Percent: {data.target_capture_percent}%\n"
                   f"  Required Mass: {data.required_mass:.2e} kg\n"
                   f"  Collector Area: {data.collector_area:.2e} m²\n"
                   "  Timeline: {data.timeline:.2f} years\n"
                   f"  Parameters:\n"
                   f"    Launch Mass Rate: {data.parameters.launch_mass_rate if data.parameters else 'N/A'} kg/year")

def parse_input(input_data: str, input_format: str = "json") -> SimulationParameters:
    """Parse input data into SimulationParameters.
    
    Args:
        input_data: String representation of input data
        input_format: Format of input data ('json' or 'cli')
        
    Returns:
        SimulationParameters object parsed from input
        
    Raises:
        ValueError: If input data is invalid or cannot be parsed
        json.JSONDecodeError: If JSON parsing fails
    """
    if not isinstance(input_data, str):
        raise ValueError("Input data must be a string")
    
    if input_format not in ["json", "cli"]:
        raise ValueError("Input format must be 'json' or 'cli'")
    
    if input_format == "json":
        try:
            data = json.loads(input_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON input: {str(e)}") from e
            
        # Validate required fields
        required_fields = ["target_capture_percent", "launch_mass_rate"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        target_capture = float(data["target_capture_percent"])
        launch_mass_rate = float(data["launch_mass_rate"])
    else:  # cli format
        # Parse CLI-style input "target_capture_percent,launch_mass_rate"
        try:
            parts = input_data.split(',')
            if len(parts) != 2:
                raise ValueError("CLI input must contain exactly 2 comma-separated values")
            
            target_capture = float(parts[0])
            launch_mass_rate = float(parts[1])
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid CLI input format: {str(e)}")
    
    # Validate values
    if not (0 <= target_capture <= 100):
        if target_capture < 0 or target_capture > 100:
            raise ValueError("Target capture percent must be between 0 and 100")
    
    if launch_mass_rate <= 0:
        raise ValueError("Launch mass rate must be positive")
    
    return SimulationParameters(target_capture_percent=target_capture, 
                             launch_mass_rate=launch_mass_rate)