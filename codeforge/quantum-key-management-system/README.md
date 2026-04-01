# Quantum Key Management System

A Python-based quantum key management library for secure inter-node communication in android embodiment frameworks. This system implements quantum key distribution protocols, edge node authentication, and performance monitoring with classical cryptography fallbacks.

## Features

- **Quantum Key Distribution (QKD)**: Implements QKD protocols for secure key exchange
- **Edge Node Authentication**: Secure authentication framework for edge nodes
- **Codonic Layer Integration**: Symbolic encoding for quantum state representation
- **Classical Fallback**: Automatic fallback to classical cryptography during quantum channel failures
- **Performance Monitoring**: Real-time latency and performance tracking for critical operations

## Prerequisites

- Python 3.8+
- pip package manager

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/quantum-key-management-system.git
cd quantum-key-management-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Setup

1. Copy the `.env.example` file to create your environment configuration:
```bash
cp .env.example .env
```

2. Configure environment variables in the `.env` file as needed

## Environment Variables

The following environment variables can be configured in the `.env` file:

```bash
# Security settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Quantum channel settings
QUANTUM_BACKEND=ibmq_qasm_simulator
QUANTUM_SHOTS=1024

# Performance monitoring
MONITORING_ENABLED=True
LATENCY_THRESHOLD_MS=100
```

## Usage Examples

### Basic QKD Implementation
```python
from src.qkd.protocol import QKDProtocol
from src.qkd.key_distribution import KeyDistribution

# Initialize QKD protocol
qkd = QKDProtocol()
key_dist = KeyDistribution(qkd)

# Generate quantum keys
keys = key_dist.generate_keys(num_keys=10)
```

### Edge Node Authentication
```python
from src.auth.edge_node_auth import EdgeNodeAuth
from src.auth.certificate_manager import CertificateManager

# Initialize authentication
auth = EdgeNodeAuth()
cert_manager = CertificateManager()

# Authenticate node
node_id = "android_node_001"
if auth.authenticate(node_id):
    print("Node authenticated successfully")
```

### Performance Monitoring
```python
from src.monitoring.performance_tracker import PerformanceTracker
from src.monitoring.latency_metrics import LatencyMetrics

# Monitor performance
tracker = PerformanceTracker()
metrics = LatencyMetrics()

# Track operation latency
tracker.start_operation("qkd_exchange")
# ... perform operation ...
tracker.end_operation("qkd_exchange")
latency = metrics.get_latency("qkd_exchange")
```

## API Documentation

### Core Modules

#### QKD Protocol (`src/qkd/protocol.py`)
- `QKDProtocol.generate_key()` - Generate quantum keys using QKD protocols
- `QKDProtocol.bb84_protocol()` - Implement BB84 quantum key distribution protocol

#### Edge Node Authentication (`src/auth/edge_node_auth.py`)
- `EdgeNodeAuth.authenticate()` - Authenticate edge nodes
- `EdgeNodeAuth.verify_credentials()` - Verify node credentials

#### Codonic Layer (`src/encoding/codonic_layer.py`)
- `CodonicLayer.encode()` - Encode quantum states symbolically
- `CodonicLayer.decode()` - Decode symbolic quantum states

## Project Structure

```
quantum-key-management-system/
├── src/
│   ├── qkd/
│   │   ├── protocol.py
│   │   ├── key_distribution.py
│   │   └── quantum_channels.py
│   ├── auth/
│   │   ├── edge_node_auth.py
│   │   └── certificate_manager.py
│   ├── encoding/
│   │   ├── codonic_layer.py
│   │   └── symbolic_encoder.py
│   ├── fallback/
│   │   ├── classical_crypto.py
│   │   └── backup_channels.py
│   ├── monitoring/
│   │   ├── performance_tracker.py
│   │   └── latency_metrics.py
│   ├── core/
│   │   ├── crypto_utils.py
│   │   ├── key_storage.py
│   │   └── quantum_utils.py
│   └── api/
│       └── key_management_api.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Testing

```bash
# Run tests (if available)
python -m pytest tests/

# Test individual modules
python -m pytest src/qkd/protocol.py
```

## Deployment

### Docker Deployment

Build and run using Docker:

```bash
# Build the Docker image
docker build -t quantum-key-management-system .

# Run the container
docker run -d --name qkms quantum-key-management-system

# Or use Docker Compose
docker-compose up -d
```

### Docker Compose

```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

```
MIT License

Copyright (c) 2024 Quantum Key Management System Contributors

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