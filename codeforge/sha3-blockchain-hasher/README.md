# SHA3 Blockchain Hasher

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library for SHA3-512 blockchain hashing with performance benchmarks and ROS2 integration capabilities.

## Features

- 🔒 **SHA3-512 Hashing**: High-performance implementation of SHA3-512 hashing algorithm
- ⚡ **Performance Benchmarking**: Built-in benchmarking utilities for performance testing
- 🤖 **ROS2 Integration**: Native support for distributed hashing through ROS2 nodes
- 📊 **Performance Analysis**: Comprehensive benchmarking with detailed metrics
- 🛠️ **Utility Functions**: Helper functions for common hashing operations
- 🐳 **Docker Support**: Containerized deployment with PostgreSQL database integration

## Prerequisites

- Python 3.8+
- Docker and Docker Compose (for containerized deployment)
- ROS2 Foxy/Focal or later (for ROS2 features)

## Installation

### Basic Installation

```bash
pip install pysha3>=1.0.0 cryptography>=3.4.0 rclpy>=3.0.0 pytest>=6.0.0 pytest-benchmark>=3.4.0
```

### From Source

```bash
git clone https://github.com/yourusername/sha3-blockchain-hasher.git
cd sha3-blockchain-hasher
pip install -r requirements.txt
```

## Environment Variables

The following environment variables can be configured:

| Variable | Description | Default |
|----------|-------------|---------|
| `ROS_DOMAIN_ID` | ROS2 domain ID for node communication | `0` |
| `HASH_ALGORITHM` | Hash algorithm selection | `sha3_512` |

## Usage Examples

### Basic Hashing

```python
from sha3_hasher.core import SHA3Hasher

# Create hasher instance
hasher = SHA3Hasher()

# Hash a simple string
data = "Hello, Blockchain!"
hash_result = hasher.hash_data(data)
print(f"Hash: {hash_result}")
```

### Using with ROS2

```python
from sha3_hasher.ros2_node import SHA3HasherNode

# Initialize ROS2 node
node = SHA3HasherNode()
node.start_hashing_service()
```

### Performance Benchmarking

```python
from sha3_hasher.benchmark import run_benchmarks

# Run performance benchmarks
results = run_benchmarks(data_size="1MB", iterations=100)
print(results)
```

## API Documentation

### Core Module

#### `SHA3Hasher` Class

```python
class SHA3Hasher:
    def hash_data(self, data: str) -> str
    def hash_file(self, file_path: str) -> str
    def verify_hash(self, data: str, expected_hash: str) -> bool
```

### Benchmarking Module

#### `run_benchmarks()` Function

```python
def run_benchmarks(data_size: str = "1KB", iterations: int = 100) -> dict
```

## Project Structure

```
sha3-blockchain-hasher/
├── sha3_hasher/
│   ├── __init__.py          # Package initialization
│   ├── core.py            # Core hashing implementation
│   ├── benchmark.py         # Benchmarking utilities
│   ├── ros2_node.py       # ROS2 node implementation
│   └── utils.py          # Utility functions
├── tests/                # Test suite
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile             # Docker configuration
└── requirements.txt         # Python dependencies
```

## Testing

### Running Tests

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=sha3_hasher tests/

# Run performance benchmarks
pytest --benchmark-only tests/benchmark_test.py
```

## Docker Compose Setup

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  sha3-hasher:
    build: .
    depends_on:
      - postgres
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/sha3_db

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=sha3_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Docker Deployment

```bash
# Build and run services
docker-compose up --build

# Run tests in container
docker-compose run sha3-hasher python -m pytest tests/
```

## Database Schema

PostgreSQL tables are automatically created for storing hash records:

```sql
CREATE TABLE hash_records (
    id SERIAL PRIMARY KEY,
    hash_value VARCHAR(128) NOT NULL,
    data_content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Your Company Name

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