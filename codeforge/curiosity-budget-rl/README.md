# Curiosity Budget RL

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A reinforcement learning library for implementing curiosity-driven budget allocation systems with dynamic skill selection and exploration-exploitation balance.

## Features

- **Curiosity-Driven Exploration**: Implements intrinsic motivation for optimal exploration strategies
- **Dynamic Budget Allocation**: Intelligent resource distribution based on skill value estimation
- **Skill Value Estimation**: Neural network-based evaluation of skill worth
- **Adaptive Reward System**: Multi-component reward mechanisms for skill selection
- **Exploration-Exploitation Balance**: Sophisticated algorithms for balancing known vs. unknown strategies
- **Reinforcement Learning Agents**: PyTorch-based agents optimized for budget allocation tasks

## Prerequisites

- Python 3.7+
- PyTorch 1.10+
- NumPy
- Gym
- Stable-Baselines3

## Installation

```bash
# Install from PyPI (when available)
pip install curiosity-budget-rl

# Or install from source
git clone https://github.com/your-username/curiosity-budget-rl.git
cd curiosity-budget-rl
pip install -e .
```

## Project Structure

```
curiosity_budget/
├── __init__.py          # Main module entry point
├── agent.py             # RL agent implementation
├── budget_manager.py    # Budget allocation logic manager
├── budget_allocator.py   # Budget distribution strategies
├── skill_selector.py     # Skill selection mechanisms
├── reward_system.py     # Reward calculation and management
├── exploration.py        # Exploration strategy implementations
├── skill_valuation.py  # Skill value estimation models
├── models.py          # Neural network architectures
└── utils.py           # Utility functions
```

## Usage Examples

```python
from curiosity_budget import CuriosityBudgetAgent
from curiosity_budget.budget_manager import BudgetManager

# Initialize the curiosity-driven agent
agent = CuriosityBudgetAgent(
    exploration_rate=0.1,
    curiosity_weight=0.5
)

# Create budget manager
budget_manager = BudgetManager(
    total_budget=1000,
    allocation_strategy='adaptive'
)

# Allocate budget based on skill values
allocations = budget_manager.allocate_budget(skills_list)
```

## API Documentation

### Core Classes

#### `CuriosityBudgetAgent`
Main reinforcement learning agent for curiosity-driven budget allocation

**Methods:**
- `train()`: Train the agent on budget allocation tasks
- `evaluate_skill_value(skill)`: Estimate the value of a given skill
- `adjust_exploration(state)`: Dynamically adjust exploration rate

#### `BudgetManager`
Handles budget allocation logic and strategy

**Methods:**
- `allocate_budget(skills, total_budget)`: Allocate budget across skills
- `update_skill_values(experience)`: Update skill value estimates
- `get_allocation_strategy()`: Retrieve current allocation approach

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test suite
python -m pytest tests/test_budget_allocation.py
```

## Environment Variables

No specific environment variables required. Configuration is handled through class initialization parameters.

## Deployment

This is a library package intended for use in other projects. For deployment:

```python
# Install as dependency
pip install curiosity-budget-rl

# Import and use in your project
import curiosity_budget
```

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install torch numpy gym stable-baselines3

# Install package in development mode
pip install -e .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Quality Note

Current quality score: 12.4/100 - This indicates significant room for improvement in code quality, documentation, and testing coverage.