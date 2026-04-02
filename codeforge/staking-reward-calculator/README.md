# Staking Reward Calculator

A Python command-line tool for calculating staking rewards with compound interest, APY, and lockup penalties.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [License](#license)

## Project Overview

This CLI tool calculates staking rewards based on:
- Annual Percentage Yield (APY) calculations
- Compound interest formulas
- Lockup period penalties
- Input validation for all parameters

## Features

- **APY Calculation**: Uses the formula `APY = (1 + (reward_rate * days/365))^365 - 1`
- **Compound Interest**: Implements `A = P*(1 + r/n)^(nt)` with configurable compounding periods
- **Lockup Penalties**: Reduces rewards for early withdrawals based on penalty percentage
- **Input Validation**: Ensures all inputs are positive numeric values
- **Command-Line Interface**: Easy-to-use CLI with argument parsing
- **Comprehensive Testing**: Full unit test coverage for all calculation paths

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/staking-reward-calculator.git
cd staking-reward-calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
python setup.py install
```

## Usage

### Command Line Interface

```bash
# Basic usage
python src/cli.py --principal 1000 --rate 0.05 --time 365 --compound 365

# With penalty parameters
python src/cli.py --principal 1000 --rate 0.05 --time 365 --compound 365 --penalty 0.1
```

### Example Commands

```bash
# Calculate rewards for 1000 stake at 5% rate over 365 days
python src/cli.py --principal 1000 --rate 0.05 --time 365

# Calculate with custom penalty
python src/cli.py --principal 1000 --rate 0.05 --time 180 --penalty 0.15
```

## API Documentation

### Core Functions

#### `calculate_apy(principal, rate, time, compound_frequency)`
Calculates APY using the formula: `APY = (1 + (rate * time/365))^(365) - 1`

#### `calculate_compound_interest(principal, rate, time, compound)`
Applies the compound interest formula: `A = P*(1 + r/n)^(nt)`

#### `apply_penalty(amount, penalty_rate)`
Applies lockup penalties when duration is less than minimum lockup period.

## Project Structure

```
staking-reward-calculator/
├── src/
│   ├── staking_calculator.py    # Core calculation logic
│   ├── cli.py                   # Command-line interface
│   └── __init__.py
├── tests/
│   ├── test_staking_calculator.py
│   └── test_cli.py
├── examples/
│   └── example_usage.py        # Example usage scripts
├── requirements.txt             # Python dependencies
├── setup.py                    # Installation configuration
└── README.md                   # Documentation
```

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Or run specific tests:
```bash
python tests/test_staking_calculator.py
python tests/test_cli.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

```
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
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
```