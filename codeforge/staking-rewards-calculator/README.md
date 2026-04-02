# Staking Rewards Calculator

A Python library for calculating staking rewards with support for APY, compound interest, and lockup penalties based on stake amount and duration.

## Features

- **APY Calculations**: Accurate annual percentage yield computations
- **Compound Interest**: Flexible compounding periods for maximum returns
- **Lockup Penalties**: Configurable penalty calculations for early withdrawals
- **Input Validation**: Robust validation for staking parameters
- **Comprehensive Testing**: Full unit test coverage for all core modules
- **Extensible Design**: Modular architecture for easy integration

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

### From PyPI (Recommended)

```bash
pip install staking-rewards-calculator
```

### From Source

```bash
# Clone the repository
git clone https://github.com/your-username/staking-rewards-calculator.git
cd staking-rewards-calculator

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Project Structure

```
staking-rewards-calculator/
├── src/
│   ├── staking_calculator.py    # Main calculation logic
│   ├── models.py                # Data models
│   ├── validators.py             # Input validation
│   └── utils.py                  # Utility functions
├── tests/
│   ├── test_staking_calculator.py
│   ├── test_models.py
│   └── test_validators.py
├── docs/
│   ├── README.md
│   └── api.md
├── requirements.txt
└── setup.py
```

## Usage Examples

### Basic Staking Reward Calculation

```python
from src.staking_calculator import StakingCalculator
from src.models import StakeParameters

# Initialize calculator
calculator = StakingCalculator()

# Create staking parameters
params = StakeParameters(
    amount=1000.0,
    duration_days=365,
    apy=0.08,  # 8% APY
    compound_frequency=365  # Daily compounding
)

# Calculate rewards
rewards = calculator.calculate_rewards(params)
print(f"Total rewards: {rewards.total_rewards}")
```

### Advanced Usage with Penalties

```python
from src.staking_calculator import StakingCalculator
from src.models import StakeParameters

calculator = StakingCalculator()

# Parameters with early withdrawal penalty
params = StakeParameters(
    amount=5000.0,
    duration_days=180,
    apy=0.12,
    compound_frequency=4,  # Quarterly compounding
    early_withdrawal_penalty=0.05  # 5% penalty
)

# Calculate with penalty applied
result = calculator.calculate_with_penalties(params, early_withdrawal_days=90)
```

## API Documentation

Detailed API documentation can be found in [docs/api.md](docs/api.md).

## Environment Variables

This library does not require any environment variables for basic operation.

## Testing

To run the test suite:

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_staking_calculator.py

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v
```

### Test Structure

```python
# Example test structure
def test_calculate_compound_interest():
    calculator = StakingCalculator()
    result = calculator.calculate_compound_interest(1000, 0.05, 365, 1)
    assert result > 1000
```

## Deployment

This is a library package intended for use in other Python projects. No specific deployment steps are required beyond installation.

### Docker Support

No Docker configuration is provided as this is a library, not a service.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues, feature requests, or questions, please open an issue on the GitHub repository.