```markdown
# Staking Reward Calculator

A Python library for calculating staking rewards with support for APY, compound interest, and lockup penalties. This library provides accurate calculations for cryptocurrency staking rewards with proper handling of edge cases.

## Features

- **APY Calculation**: Accurate Annual Percentage Yield calculations
- **Compound Interest**: Support for compounding rewards over time
- **Lockup Penalties**: Apply penalties for early withdrawal based on stake duration
- **Edge Case Handling**: Proper validation for zero stakes, negative values, and invalid inputs
- **Comprehensive Testing**: Full test coverage with pytest
- **Input Validation**: Robust error handling for all calculation functions

## Prerequisites

- Python 3.6+
- pip (Python package installer)

## Installation

### From PyPI

```bash
pip install staking-reward-calculator
```

### From Source

```bash
git clone https://github.com/yourusername/staking-reward-calculator.git
cd staking-reward-calculator
pip install -r requirements.txt
```

### Development Installation

```bash
pip install -e .
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Examples

```python
from src.staking_calculator import StakingCalculator

# Initialize calculator
calculator = StakingCalculator()

# Calculate simple staking reward
reward = calculator.calculate_reward(
    principal=1000,
    apr=0.08,  # 8% annual rate
    duration_days=365
)
print(f"Reward: {reward}")

# Calculate compound interest
compound_reward = calculator.calculate_compound_reward(
    principal=1000,
    apr=0.08,
    duration_days=365,
    compound_frequency=30  # Compound monthly
)

# Apply lockup penalty
final_reward = calculator.apply_lockup_penalty(
    reward=100,
    lockup_days=90,
    elapsed_days=30  # Early withdrawal after 30 days
)
```

## API Documentation

### StakingCalculator Class

#### `calculate_reward(principal, apr, duration_days)`
Calculate simple staking reward
- **principal**: Initial stake amount
- **apr**: Annual percentage rate (as decimal, e.g., 0.08 for 8%)
- **duration_days**: Stake duration in days
- **Returns**: Calculated reward amount

#### `calculate_compound_reward(principal, apr, duration_days, compound_frequency)`
Calculate compound interest reward
- **compound_frequency**: Compounding period in days

#### `apply_lockup_penalty(reward, lockup_days, elapsed_days)`
Apply early withdrawal penalty
- **lockup_days**: Required lockup period
- **elapsed_days**: Time elapsed since staking

## Project Structure

```
staking-reward-calculator/
├── src/
│   └── staking_calculator.py     # Core calculation logic
├── tests/
│   └── test_staking_calculator.py # Test suite
├── setup.py                      # Package configuration
├── requirements.txt                # Dependencies
└── README.md                    # This file
```

## Testing

Run the full test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

## Environment Variables

This library does not require any environment variables for basic operation.

## Deployment

This is a library package and does not require deployment. To use in your project:

1. Install via pip:
   ```bash
   pip install staking-reward-calculator
   ```

2. Import and use:
   ```python
   from staking_calculator import StakingCalculator
   ```

## License

MIT License

Copyright (c) 2023 Staking Reward Calculator Contributors

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