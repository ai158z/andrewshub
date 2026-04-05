# Ed25519 Blockchain ROS2 Verifier

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)

A Python library for Ed25519 signature verification with support for blockchain transaction validation and ROS2 robotics integration.

## Features

- ✅ **Ed25519 Signature Verification**: Robust cryptographic signature validation
- 🔗 **Blockchain Integration**: Verify signatures in blockchain transactions
- 🤖 **ROS2 Support**: Native integration with Robot Operating System 2
- 📦 **Modular Design**: Clean separation of core, blockchain, and robotics components
- 🧪 **Comprehensive Testing**: Full test suite for all verification components
- 🐳 **Docker Support**: Containerized environment for consistent deployment

## Prerequisites

- Python 3.7 or higher
- ROS2 (Foxy, Galactic, or Humble recommended)
- Basic understanding of cryptographic signatures
- Docker (for containerized deployment)

## Installation

### From PyPI

```bash
pip install ed25519-blockchain-ros2-verifier
```

### From Source

```bash
git clone https://github.com/yourusername/ed25519-blockchain-ros2-verifier.git
cd ed25519-blockchain-ros2-verifier
pip install -r requirements.txt
python setup.py install
```

### Docker Installation

```bash
docker build -t ed25519-verifier .
docker run -it ed25519-verifier python examples/basic_usage.py
```

## Environment Variables

No required environment variables. All configuration is handled through the API.

## Usage Examples

### Basic Signature Verification

```python
from ed25519_verifier.core import verify_signature
from ed25519_verifier.utils import generate_keypair

# Generate a keypair
private_key, public_key = generate_keypair()

# Create and verify signature
message = b"Hello, World!"
signature = private_key.sign(message)
is_valid = verify_signature(public_key, message, signature)
```

### Blockchain Transaction Verification

```python
from ed25519_verifier.blockchain import verify_transaction

# Verify a blockchain transaction
transaction_data = {
    'from': 'sender_public_key',
    'to': 'recipient_address',
    'amount': 100,
    'signature': 'transaction_signature'
}

is_valid = verify_transaction(transaction_data)
```

### ROS2 Sensor Data Verification

```python
from ed25519_verifier.ros2_integration import verify_sensor_data

# Verify sensor data from ROS2 nodes
sensor_data = {
    'timestamp': 1234567890,
    'sensor_id': 'lidar_001',
    'data': 'sensor_readings',
    'signature': 'data_signature'
}

is_verified = verify_sensor_data(sensor_data)
```

## API Documentation

### Core Module (`ed25519_verifier.core`)

#### `verify_signature(public_key, message, signature)`
Verifies an Ed25519 signature against a message and public key.

**Parameters:**
- `public_key` (bytes): The public key for verification
- `message` (bytes): The original message
- `signature` (bytes): The signature to verify

**Returns:** `bool` - True if signature is valid

### Blockchain Module (`ed25519_verifier.blockchain`)

#### `verify_transaction(transaction_dict)`
Verifies blockchain transaction signatures.

**Parameters:**
- `transaction_dict` (dict): Transaction data with signature

**Returns:** `bool` - Transaction validity

### ROS2 Integration Module (`ed25519_verifier.ros2_integration`)

#### `verify_sensor_data(data_dict)`
Verifies ROS2 sensor data signatures.

**Parameters:**
- `data_dict` (dict): Sensor data with signature

**Returns:** `bool` - Data integrity status

## Project Structure

```
ed25519-blockchain-ros2-verifier/
├── ed25519_verifier/
│   ├── __init__.py
│   ├── core.py
│   ├── blockchain.py
│   ├── ros2_integration.py
│   ├── utils.py
│   └── exceptions.py
├── tests/
│   ├── test_core.py
│   ├── test_blockchain.py
│   └── test_ros2_integration.py
├── examples/
│   ├── basic_usage.py
│   ├── blockchain_transaction_demo.py
│   └── ros2_sensor_example.py
├── requirements.txt
├── setup.py
└── Dockerfile
```

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Or using unittest:

```bash
python -m unittest discover tests/
```

## Deployment

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t ed25519-verifier .
```

2. Run in container:
```bash
docker run -it ed25519-verifier
```

### Local Development

```bash
# Install in development mode
pip install -e .

# Run examples
python examples/basic_usage.py
python examples/blockchain_transaction_demo.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```