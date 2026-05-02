# Dyson Swarm Simulator

A physics-grounded CLI tool for simulating Dyson swarm construction timelines. This simulator calculates the time, mass, and area requirements for capturing a target percentage of solar energy using space-based solar collectors.

## Features

- **Physics-based modeling**: Grounded in real astrophysical constants and engineering parameters
- **Configurable parameters**: Customizable target solar capture percentage and launch mass rate
- **Realistic constraints**: Accounts for material limitations from asteroid mining (using Psyche as reference)
- **JSON output**: Machine-readable results for integration with other tools
- **Comprehensive CLI**: User-friendly command-line interface with help and validation

## Prerequisites

- Python 3.7+
- pip package manager

## Installation

### From PyPI
```bash
pip install dyson-swarm-simulator
```

### From Source
```bash
git clone https://github.com/your-username/dyson-swarm-simulator.git
cd dyson-swarm-simulator
pip install -r requirements.txt
```

## Environment Variables

No environment variables required.

## Usage

### Basic Usage
```bash
python -m dyson_simulator --target_pct 1.0 --launch_rate 1e8
```

### With JSON Output
```bash
python -m dyson_simulator --target_pct 0.01 --launch_rate 1e8 --json
```

### Command Line Options
```
--target_pct FLOAT    Target percentage of solar energy to capture (default: 1.0)
--launch_rate FLOAT   Launch mass rate in kg/year (default: 1e8)
--json                Output results in JSON format
--help                Show help message
```

## API Documentation

### Core Parameters
- **target_pct**: Desired percentage of solar energy to capture (0.01% to 100%)
- **launch_rate**: Annual mass launch capability in kg/yr

### Physical Constants (from SPIRIT.md)
- Solar luminosity: 3.8×10²⁶ W
- Asteroid Psyche mass: 2.3×10¹⁹ kg
- Main belt asteroid mass: 3×10²¹ kg
- Collector mass density: 0.5 kg/m²
- Solar panel efficiency: 40%
- Solar constant: 1366 W/m²

## Project Structure

```
dyson-swarm-simulator/
├── dyson_simulator/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── cli.py           # CLI interface
│   ├── calculations.py    # Core physics calculations
│   ├── models.py        # Data models
│   ├── constants.py       # Physical constants
│   └── utils.py        # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_calculations.py
│   └── test_models.py
├── requirements.txt
└── setup.py
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test module
python -m pytest tests/test_calculations.py
```

## Deployment

### Docker Deployment
No Docker configuration provided.

### Systemd Service
No systemd service configuration provided.

## Built on Foundations

- **Dyson (1960)**: "Search for Artificial Stellar Sources of Infrared Radiation"
- **Criswell & Waldron**: Lunar-based power systems research
- **NASA Psyche Mission**: Asteroid 16 Psyche exploration and resource assessment

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Based on theoretical work by:
- Freeman Dyson (1960)
- David Criswell and Wendell Waldron (lunar power systems)
- NASA Psyche mission team (asteroid resource assessment)

---

*Note: This is a simulation tool for research purposes. Actual Dyson swarm construction remains highly speculative and faces significant engineering challenges.*