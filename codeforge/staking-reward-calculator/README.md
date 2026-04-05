# Staking Reward Calculator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool for calculating staking rewards with comprehensive analysis and visualization capabilities.

## Features

- **Stake Calculation**: Calculate estimated staking rewards based on current network parameters
- **Reward Visualization**: Generate time-series visualizations of reward growth
- **Risk Analysis**: Include risk factors affecting potential rewards (network changes, validator performance)
- **Currency Conversion**: Automatic USD equivalent calculation using current market prices
- **Multiple Networks**: Support for various blockchain networks
- **Comprehensive Reporting**: Detailed output with risk assessments and projections

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/staking-reward-calculator.git
cd staking-reward-calculator

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Using pip

```bash
pip install staking-reward-calculator
```

## Project Structure

```
staking-reward-calculator/
├── src/
│   ├── cli.py              # CLI entry point
│   ├── calculator.py        # Core calculation logic
│   ├── visualizer.py       # Reward visualization
│   ├── risk_analyzer.py    # Risk analysis logic
│   ├── network_data.py     # Network data fetching
│   └── currency_converter.py # Currency conversion
├── tests/
│   ├── test_calculator.py
│   ├── test_visualizer.py
│   ├── test_risk_analyzer.py
│   ├── test_network_data.py
│   └── test_currency_converter.py
├── requirements.txt
└── setup.py
```

## Usage

### Basic Usage

```bash
# Calculate staking rewards
python -m src.cli --stake 1000 --duration 365 --network ethereum

# With risk analysis
python -m src.cli --stake 5000 --duration 180 --network cosmos --include-risk
```

### Command Line Options

```bash
python -m src.cli [OPTIONS]

Options:
  --stake FLOAT                   Amount to stake
  --duration INTEGER                Staking duration in days
  --network TEXT                  Blockchain network (ethereum, cosmos, etc.)
  --include-risk                  Include risk analysis in calculation
  --currency TEXT                  Output currency (USD, EUR, etc.)
  --help                         Show this message and exit
```

## API Documentation

### Core Modules

#### `calculator.py`
```python
def calculate_rewards(stake_amount: float, duration: int, network: str) -> dict:
    """
    Calculate staking rewards based on network parameters
    
    Args:
        stake_amount: Amount to stake
        duration: Staking period in days
        network: Target blockchain network
        
    Returns:
        dict: Reward calculation results
    """
```

#### `network_data.py`
```python
def fetch_network_parameters(network: str) -> dict:
    """
    Fetch current network parameters from external APIs
    
    Args:
        network: Blockchain network identifier
        
    Returns:
        dict: Current network parameters
    """
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test modules
python -m pytest tests/test_calculator.py
python -m pytest tests/test_visualizer.py
```

## Deployment

### Docker Deployment (Optional)

If using Docker for containerized deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-m", "src.cli"]
```

### Environment Variables

No specific environment variables required. All configuration is handled via command-line arguments.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 staking-reward-calculator

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```