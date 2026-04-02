# Staking Reward Calculator

A Python CLI tool for calculating staking rewards with compound interest, APY, and lockup penalties.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- Calculate Annual Percentage Yield (APY) based on stake amount and duration
- Compute compound interest with monthly compounding
- Apply lockup penalties for early withdrawals
- Command-line interface for easy usage
- Comprehensive unit testing with generated test scenarios
- Docker support for containerized deployment

## Prerequisites

- Python 3.7 or higher
- pip package manager

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
docker run staking-reward-calculator --help
```

## Environment Variables

Copy the example environment file and customize as needed:

```bash
cp .env.example .env
```

Key environment variables:
- `DEFAULT_REWARD_RATE`: Default reward rate for calculations (default: 0.05)
- `COMPOUNDING_PERIODS`: Number of compounding periods per year (default: 12)

## Usage

### Command Line Interface

```bash
python src/main.py --amount AMOUNT --duration DAYS --lockup LOCKUP_PERCENTAGE
```

**Arguments:**
- `--amount` or `-a`: Stake amount in USD (required)
- `--duration` or `-d`: Staking duration in days (required)
- `--lockup` or `-l`: Lockup penalty percentage (required)

**Example:**
```bash
python src/main.py --amount 10000 --duration 365 --lockup 5
```

### Output Example

```
Staking Reward Calculation Results:
--------------------------------
Stake Amount: $10,000.00
Duration: 365 days
APY: 5.12%
Gross Rewards: $512.00
Lockup Penalty (5%): $512.00
Net Rewards: $460.80
Total Value: $10,460.80
```

## Project Structure

```
staking-reward-calculator/
├── src/
│   ├── main.py              # Application entry point
│   ├── staking_calculator.py # Core calculation logic
│   └── cli.py              # CLI parsing logic
├── tests/
│   ├── test_calculator.py    # Unit tests
│   ├── generate_test_data.py  # Test data generation
│   └── test_data.csv       # Test scenarios
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── .env.example             # Environment variables example
└── README.md              # This file
```

## Testing

Run all tests:

```bash
python -m pytest tests/ -v
```

Generate new test data:

```bash
python tests/generate_test_data.py
```

## API Documentation

### Core Functions

**calculate_apy(reward_rate, days)**
Calculates Annual Percentage Yield
- Parameters:
  - `reward_rate` (float): Annual reward rate (e.g., 0.05 for 5%)
  - `days` (int): Staking duration in days
- Returns: `float` - APY as decimal

**calculate_compound_interest(principal, rate, days)**
Calculates compound interest with monthly compounding
- Parameters:
  - `principal` (float): Initial stake amount
  - `rate` (float): Annual interest rate
  - `days` (int): Investment duration in days
- Returns: `float` - Final amount after compounding

**apply_lockup_penalty(amount, penalty_percentage)**
Applies lockup penalty to rewards
- Parameters:
  - `amount` (float): Amount to apply penalty to
  - `penalty_percentage` (float): Penalty percentage (0-100)
- Returns: `tuple` - (penalty_amount, net_amount)

## Deployment

### Docker Deployment

1. Build the image:
```bash
docker build -t staking-reward-calculator .
```

2. Run calculations:
```bash
docker run staking-reward-calculator --amount 5000 --duration 180 --lockup 3
```

### Production Deployment

For production use, consider:
- Setting up proper logging
- Adding input validation for edge cases
- Implementing configuration management
- Setting up monitoring and alerting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT License

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