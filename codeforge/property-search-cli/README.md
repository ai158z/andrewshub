# Property Search CLI

A complete property search CLI tool that filters properties based on various criteria with robust input validation and type conversion.

## Features

- **Type Conversion**: Automatically converts numeric strings to appropriate types (int/float)
- **CLI Argument Parsing**: Full command-line interface with comprehensive argument parsing
- **Input Validation**: Validates numeric inputs and percentage ranges with proper error handling
- **Property Filtering**: Search properties by price, bedrooms, bathrooms, location, and other criteria
- **Unit Testing**: Complete test coverage for all components
- **Error Handling**: Comprehensive error handling for invalid inputs and edge cases

## Prerequisites

- Python 3.6+
- pip (Python package installer)

## Installation

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/property-search-cli.git
cd property-search-cli

# Install dependencies
pip install -r requirements.txt
```

### Using setup.py

```bash
# Clone the repository
git clone https://github.com/yourusername/property-search-cli.git
cd property-search-cli

# Install the package
pip install -e .
```

## Usage

```bash
# Basic usage
python src/main.py --min-price 100000 --max-price 500000 --location "New York"

# Search with multiple criteria
python src/main.py --min-price 200000 --max-bedrooms 3 --min-bathrooms 2 --property-type "house"

# Using percentage ranges
python src/main.py --price-drop-min 5 --price-drop-max 15
```

### Command Line Arguments

| Argument | Description | Type | Example |
|---------|-------------|------|---------|
| `--min-price` | Minimum property price | Integer | `--min-price 100000` |
| `--max-price` | Maximum property price | Integer | `--max-price 500000` |
| `--min-bedrooms` | Minimum number of bedrooms | Integer | `--min-bedrooms 2` |
| `--max-bedrooms` | Maximum number of bedrooms | Integer | `--max-bedrooms 5` |
| `--min-bathrooms` | Minimum number of bathrooms | Float | `--min-bathrooms 1.5` |
| `--location` | Property location/city | String | `--location "New York"` |
| `--property-type` | Type of property | String | `--property-type house` |
| `--price-drop-min` | Minimum price drop percentage | Integer (0-100) | `--price-drop-min 10` |
| `--price-drop-max` | Maximum price drop percentage | Integer (0-100) | `--price-drop-max 30` |

## Project Structure

```
property-search-cli/
├── src/
│   ├── main.py              # Entry point
│   ├── property_search.py     # Core search logic
│   ├── cli_parser.py        # Argument parsing
│   ├── validators.py         # Input validation
│   └── utils.py           # Utility functions
├── tests/
│   ├── test_property_search.py
│   ├── test_cli_parser.py
│   ├── test_validators.py
│   ├── test_utils.py
│   └── __init__.py
├── requirements.txt          # Dependencies
├── setup.py               # Package configuration
└── README.md              # This file
```

## Testing

Run all tests:

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_validators.py

# Run with coverage
pytest --cov=src tests/
```

## API Documentation

### Core Functions

#### Property Search
```python
def search_properties(criteria: dict) -> list
```
Filters properties based on search criteria.

**Parameters:**
- `criteria` (dict): Search criteria including price range, bedrooms, bathrooms, etc.

**Returns:**
- `list`: Filtered properties matching criteria

#### Input Validation
```python
def validate_numeric_input(value: str, min_val: float = None, max_val: float = None) -> Union[int, float]
```
Converts and validates numeric input strings.

**Parameters:**
- `value` (str): Input string to validate
- `min_val` (float): Minimum allowed value
- `max_val` (float): Maximum allowed value

**Returns:**
- `int/float`: Converted numeric value

#### CLI Parser
```python
def parse_arguments() -> argparse.Namespace
```
Parses command line arguments with validation.

**Returns:**
- `argparse.Namespace`: Parsed arguments

## Deployment

This is a CLI application that runs locally. No special deployment required.

## License

MIT License

Copyright (c) 2024

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