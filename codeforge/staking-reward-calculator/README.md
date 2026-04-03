# Staking Reward Calculator

A Python library for calculating staking rewards with APY, compound interest, and lockup penalties. This tool provides precise financial calculations for cryptocurrency staking scenarios with detailed reward estimates.

## Features

- **APY Calculation**: Accurate Annual Percentage Yield calculations with configurable compounding frequencies
- **Compound Interest**: Support for various compounding periods (daily, weekly, monthly, annually)
- **Lockup Penalties**: Calculate penalties for early unstaking with configurable penalty structures
- **High Precision**: Uses Python's `decimal` module for financial-grade precision
- **Input Validation**: Comprehensive validation for all staking parameters
- **Detailed Results**: Breakdown of rewards, penalties, and effective returns

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

### From PyPI
```bash
pip install staking-reward-calculator
```

### From Source
```bash
git clone https://github.com/your-username/staking-reward-calculator.git
cd staking-reward-calculator
pip install -r requirements.txt
```

### Development Installation
```bash
pip install -e .
```

## Usage Examples

### Basic Usage
```python
from staking_calculator import calculate_staking_rewards

# Calculate rewards for 1000 tokens staked for 1 year at 10% APY
result = calculate_staking_rewards(
    stake_amount=1000.0,
    duration_days=365,
    annual_percentage_yield=10.0,
    compounding_frequency='daily'
)

print(f"Total Rewards: {result.total_rewards}")
print(f"Final Amount: {result.final_amount}")
```

### With Early Unstaking Penalty
```python
from staking_calculator import calculate_staking_with_penalty

# Calculate with 25% penalty for early withdrawal after 90 days
result = calculate_staking_with_penalty(
    stake_amount=5000.0,
    duration_days=90,
    annual_percentage_yield=8.5,
    penalty_rate=0.25,
    penalty_applies_before_days=180
)

print(f"Rewards After Penalty: {result.rewards_after_penalty}")
print(f"Penalty Amount: {result.penalty_amount}")
```

## API Documentation

### Main Functions

#### `calculate_staking_rewards()`
Calculate staking rewards with compound interest

**Parameters:**
- `stake_amount` (float): Initial amount staked
- `duration_days` (int): Staking duration in days
- `annual_percentage_yield` (float): Annual yield percentage
- `compounding_frequency` (str): Compounding period ('daily', 'weekly', 'monthly', 'annually')
- `decimal_precision` (int, optional): Decimal precision for calculations

**Returns:**
`StakingResult` object with:
- `total_rewards`: Total accumulated rewards
- `final_amount`: Final stake value
- `effective_apr`: Effective annual percentage rate
- `compounding_details`: Breakdown of compounding calculations

#### `calculate_staking_with_penalty()`
Calculate staking rewards including early withdrawal penalties

**Parameters:**
- `stake_amount` (float): Initial amount staked
- `duration_days` (int): Actual staking duration
- `annual_percentage_yield` (float): Annual yield percentage
- `penalty_rate` (float): Penalty rate as decimal (0.25 = 25%)
- `penalty_applies_before_days` (int): Days before which penalty applies
- `compounding_frequency` (str): Compounding period

**Returns:**
`PenaltyResult` object with additional penalty information

## Project Structure

```
staking-reward-calculator/
├── staking_calculator/
│   ├── __init__.py
│   ├── core.py          # Core calculation engine
│   ├── models.py         # Data models
│   ├── calculator.py     # Main calculator logic
│   ├── validators.py      # Input validation
│   └── utils.py        # Utility functions
├── tests/
│   ├── test_calculator.py
│   ├── test_compounding.py
│   └── test_penalties.py
├── requirements.txt
├── setup.py
└── README.md
```

## Testing

Run all tests:
```bash
python -m pytest tests/
```

Run specific test modules:
```bash
python -m pytest tests/test_calculator.py
python -m pytest tests/test_compounding.py
python -m pytest tests/test_penalties.py
```

Run tests with coverage:
```bash
python -m pytest --cov=staking_calculator tests/
```

## Environment Variables

This library does not require environment variables for basic operation. All configuration is passed through function parameters.

## Deployment

This is a library package. For deployment in applications:

1. Install via pip: `pip install staking-reward-calculator`
2. Import in your Python code: `from staking_calculator import calculate_staking_rewards`
3. Use the calculation functions in your application logic

## License

MIT License

Copyright (c) 2023 Your Name

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