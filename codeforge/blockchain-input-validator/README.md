# Blockchain Input Validator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

A comprehensive input validation framework for blockchain applications with threat detection, transaction format validation, address verification, and ROS2 integration for embedded systems.

## Features

- ✅ **Multi-blockchain Support**: Ethereum, Bitcoin, and generic blockchain validation
- 🔍 **Threat Detection**: Advanced security threat analysis for transactions
- 📦 **Transaction Validation**: Comprehensive transaction format and structure validation
- 📍 **Address Verification**: Cross-blockchain address format verification
- 🤖 **ROS2 Integration**: Native support for embedded systems via ROS2 bridge
- 🛡️ **Security Rules**: Built-in semantic and syntactic security validation rules

## Prerequisites

- Python 3.8+
- ROS2 (Foxy or newer recommended)
- pip 21.0+

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/blockchain-input-validator.git
cd blockchain-input-validator

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install .
```

### Development Installation

```bash
# Install in development mode
pip install -e .
```

## Environment Variables

No environment variables are required for basic operation.

## Usage Examples

### Basic Transaction Validation

```python
from blockchain_validator import BlockchainValidator

validator = BlockchainValidator()

# Validate Ethereum transaction
tx_data = {
    "from": "0x742d35Cc6F283981898339520543234712345678",
    "to": "0x8eB9C2de6554912C51146542052F1A811B738032",
    "value": "1000000000000000000",
    "gas": "21000",
    "gasPrice": "20000000000"
}

is_valid = validator.validate_transaction("ethereum", tx_data)
print(f"Transaction valid: {is_valid}")
```

### Address Verification

```python
from blockchain_validator import AddressVerifier

verifier = AddressVerifier()

# Verify Bitcoin address
is_valid = verifier.verify_address("bitcoin", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
print(f"Address valid: {is_valid}")
```

### Threat Detection

```python
from blockchain_validator import ThreatDetector

detector = ThreatDetector()
threats = detector.analyze_transaction({
    "from": malicious_address,
    "data": suspicious_data
})
```

## API Documentation

### Core Classes

#### `BlockchainValidator`
Main validation interface for blockchain data.

**Methods:**
- `validate_transaction(chain_type: str, transaction_data: dict)` - Validate transaction structure
- `validate_address(chain_type: str, address: str)` - Verify blockchain address format
- `detect_threats(transaction_data: dict)` - Analyze for security threats

#### `AddressVerifier`
Blockchain address verification utility.

**Methods:**
- `verify_address(chain_type: str, address: str)` - Verify address for specific blockchain

#### `ThreatDetector`
Security threat analysis engine.

**Methods:**
- `analyze_transaction(transaction_data: dict)` - Analyze transaction for threats

## Project Structure

```
blockchain-input-validator/
├── blockchain_validator/
│   ├── __init__.py
│   ├── core.py
│   ├── validator.py
│   ├── threat_detector.py
│   ├── transaction_validator.py
│   ├── address_verifier.py
│   ├── ros2_bridge.py
│   ├── formats/
│   │   ├── __init__.py
│   │   ├── ethereum.py
│   │   ├── bitcoin.py
│   │   └── generic.py
│   └── rules/
│       ├── __init__.py
│       ├── syntax.py
│       ├── semantics.py
│       └── security.py
├── tests/
├── requirements.txt
└── setup.py
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test module
python -m pytest tests/test_validator.py
```

### Test Structure

```
tests/
├── test_core.py
├── test_validator.py
├── test_threat_detector.py
├── test_transaction_validator.py
├── test_address_verifier.py
└── test_formats/
    ├── test_ethereum.py
    ├── test_bitcoin.py
    └── test_generic.py
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

RUN pip install .
```

### ROS2 Integration

```python
from blockchain_validator.ros2_bridge import ROS2Bridge

bridge = ROS2Bridge()
bridge.start_validation_node()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Blockchain Input Validator Contributors

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