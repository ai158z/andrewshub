# JSON to CSV Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python command-line tool for converting JSON data to CSV format with advanced features including field mapping, error handling, and specialized blockchain data support.

## Features

- **JSON to CSV Conversion**: Convert complex JSON structures to flat CSV format
- **Field Mapping**: Custom field mapping for nested JSON objects
- **Error Handling**: Comprehensive validation and error reporting
- **Blockchain Support**: Specialized parsing for blockchain transaction and block data
- **Schema Validation**: JSON schema validation for input data integrity
- **Command Line Interface**: Intuitive CLI with multiple configuration options

## Prerequisites

- Python 3.7+
- pip package manager

## Installation

### Using pip

```bash
pip install json-to-csv-converter
```

### From source

```bash
git clone https://github.com/yourusername/json-to-csv-converter.git
cd json-to-csv-converter
pip install -r requirements.txt
```

### Development Installation

```bash
pip install -e .
```

## Environment Variables

No environment variables are required for basic operation.

## Usage

### Basic Conversion

```bash
# Convert JSON file to CSV
python -m src.main input.json -o output.csv

# With custom field mapping
python -m src.main input.json -o output.csv --field-map "id:user_id,name:username"

# With schema validation
python -m src.main input.json -o output.csv --schema schema.json
```

### Command Line Options

```bash
# Basic usage
json-to-csv-converter input.json -o output.csv

# Specify field mapping
json-to-csv-converter input.json -o output.csv --field-map "old_field:new_field,another_old:another_new"

# Enable blockchain parsing mode
json-to-csv-converter input.json -o output.csv --blockchain-mode

# With JSON schema validation
json-to-csv-converter input.json -o output.csv --schema schema.json
```

## API Documentation

### Main Modules

#### `src/main.py`
Entry point for CLI application orchestrating the conversion process

#### `src/converter.py`
Core conversion logic for transforming JSON to CSV with field mapping and flattening capabilities

#### `src/validators.py`
Validation functions for:
- Input JSON data validation
- Schema validation using jsonschema
- Data integrity checks

#### `src/blockchain_parser.py`
Specialized parser for blockchain data structures:
- Transaction data parsing
- Block data processing
- Smart contract event handling

#### `src/cli_parser.py`
Command-line interface using Click:
- Argument parsing
- Option handling
- Help documentation

#### `src/utils.py`
Utility functions for:
- Data manipulation
- File handling
- JSON flattening
- Error handling utilities

## Project Structure

```
json-to-csv-converter/
├── src/
│   ├── main.py              # Entry point
│   ├── converter.py          # Core conversion logic
│   ├── validators.py         # Data validation
│   ├── blockchain_parser.py  # Blockchain data parser
│   ├── cli_parser.py        # CLI argument parser
│   └── utils.py           # Utility functions
├── tests/
│   ├── test_converter.py
│   ├── test_validators.py
│   ├── test_blockchain_parser.py
│   └── test_cli_parser.py
├── requirements.txt
├── setup.py
└── README.md
```

## Testing

### Run All Tests

```bash
python -m pytest tests/ -v
```

### Run Specific Test Modules

```bash
# Test converter module
python -m pytest tests/test_converter.py -v

# Test validators
python -m pytest tests/test_validators.py -v

# Test blockchain parser
python -m pytest tests/test_blockchain_parser.py -v

# Test CLI parser
python -m pytest tests/test_cli_parser.py -v
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  json-to-csv:
    build: .
    volumes:
      - ./data:/app/data
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
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
```