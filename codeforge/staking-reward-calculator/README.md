# Staking Reward Calculator

A command-line interface (CLI) tool for calculating staking rewards with support for APY, compound interest, and lockup penalties. This calculator helps users estimate their staking returns based on principal amount, annual percentage rate, staking duration, and lockup periods.

## Features

- **APY Calculation**: Calculate annual percentage yield with compounding interest
- **Compound Interest**: Support for compounding staking rewards over time
- **Lockup Penalties**: Calculate penalties for early withdrawal during lockup periods
- **Input Validation**: Robust validation and type conversion for all inputs
- **CLI Interface**: User-friendly command-line interface with clear options
- **Docker Support**: Containerized application for easy deployment

## Prerequisites

- Python 3.7 or higher
- pip package manager
- Docker (optional, for containerized deployment)

## Installation

### Local Installation

```bash
# Clone the repository
git clone <repository-url>
cd staking-reward-calculator

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Docker Installation

```bash
# Build the Docker image
docker build -t staking-reward-calculator .

# Run the container
docker run staking-reward-calculator --principal 1000 --apr 0.05 --duration 365 --lockup 30
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# .env.example
DEFAULT_PRINCIPAL=1000
DEFAULT_APR=0.08
DEFAULT_DURATION=365
DEFAULT_LOCKUP=30
```

## Usage

### Basic Usage

```bash
# Calculate staking rewards
python src/main.py --principal 1000 --apr 0.05 --duration 365 --lockup 30

# With partial parameters (using defaults for others)
python src/main.py --principal 5000 --duration 180
```

### Command Line Arguments

```bash
python src/main.py --help
```

- `--principal`: Principal amount for staking (default: 1000)
- `--apr`: Annual Percentage Rate as decimal (default: 0.08)
- `--duration`: Staking duration in days (default: 365)
- `--lockup`: Lockup period in days (default: 30)

### Examples

```bash
# Example 1: Basic calculation
python src/main.py --principal 10000 --apr 0.12 --duration 365 --lockup 90

# Example 2: Minimum staking period
python src/main.py --principal 500 --duration 30

# Example 3: No lockup penalty
python src/main.py --principal 2000 --apr 0.06 --duration 180 --lockup 0
```

## API Documentation

This is a CLI-only application, so there is no web API. The core calculation functions can be imported and used programmatically:

```python
from src.staking_calculator import calculate_staking_rewards

result = calculate_staking_rewards(
    principal=1000,
    apr=0.05,
    duration=365,
    lockup=30
)
```

## Project Structure

```
staking-reward-calculator/
├── src/
│   ├── main.py              # Application entry point
│   ├── cli.py               # CLI argument parsing
│   ├── staking_calculator.py # Core calculation logic
│   ├── validator.py           # Input validation utilities
│   └── types.py            # Type definitions and conversion
├── tests/
│   ├── test_staking_calculator.py
│   └── test_cli.py
├── Dockerfile               # Docker configuration
├── requirements.txt           # Python dependencies
├── .env.example            # Environment variable template
└── README.md              # This file
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test file
python -m pytest tests/test_staking_calculator.py
```

## Deployment

### Docker Deployment

```bash
# Build and run with Docker
docker build -t staking-calculator .
docker run staking-calculator --principal 1000 --apr 0.05 --duration 365

# Run with environment variables
docker run -it --env-file .env staking-calculator
```

### Local Deployment

```bash
# Make the script executable
chmod +x src/main.py

# Run directly
./src/main.py --principal 2000 --duration 180
```

## License

MIT License

Copyright (c) 2024 Staking Reward Calculator Project

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