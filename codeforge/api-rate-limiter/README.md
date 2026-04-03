# API Rate Limiter

A Flask middleware library that implements rate limiting for API endpoints using the sliding window algorithm with Redis integration.

## Features

- **Sliding Window Algorithm**: Implements precise rate limiting using a time-based sliding window approach
- **Redis Integration**: Stores rate limiting data in Redis with automatic expiration
- **Automatic Endpoint Discovery**: Scans and identifies all public API endpoints for rate limiting
- **Configurable Limits**: Default 100 requests per minute per IP address
- **Automatic Cleanup**: Redis data expires after 1 hour
- **Proper HTTP Responses**: Returns 429 Too Many Requests with Retry-After header
- **Comprehensive Logging**: Tracks rate-limited requests with IP, timestamp, and limit details
- **Docker Support**: Containerized deployment with Docker Compose

## Prerequisites

- Python 3.7+
- Redis server
- Docker and Docker Compose (for containerized deployment)

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd api-rate-limiter
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env file with your configuration
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
RATE_LIMIT=100
RATE_WINDOW=60
```

## Setup & Configuration

### Quick Start with Docker Compose

```bash
# Start Redis and the rate limiter service
docker-compose up -d

# Run tests
docker-compose exec app python -m pytest tests/
```

### Manual Setup

1. Start Redis server:
```bash
redis-server
```

2. Run the application:
```bash
python src/main.py
```

## Usage Examples

### Basic Integration

```python
from flask import Flask
from src.middleware import setup_rate_limiter

app = Flask(__name__)
setup_rate_limiter(app)

@app.route('/api/users')
def get_users():
    return {"users": []}

if __name__ == '__main__':
    app.run(debug=True)
```

### Testing Rate Limits

```python
# Test the rate limiter
import requests

# Make 100 rapid requests to test the limit
for i in range(150):
    response = requests.get('http://localhost:5000/api/test')
    if response.status_code == 429:
        print(f"Rate limited at request {i}")
        break
```

## API Documentation

The rate limiter automatically applies to all registered endpoints. When a client exceeds the rate limit:
- HTTP 429 Too Many Requests response
- `Retry-After` header indicates when the client can retry
- All requests are logged with IP, timestamp, and limit information

## Project Structure

```
api-rate-limiter/
├── src/
│   ├── rate_limiter.py          # Core rate limiting logic
│   ├── redis_client.py         # Redis connection management
│   ├── middleware.py            # Flask middleware implementation
│   ├── utils/
│   │   └── endpoint_scanner.py  # Automatic endpoint discovery
│   ├── config/
│   │   └── rate_limit_config.py # Configuration module
│   └── main.py                   # Application entry point
├── tests/
│   ├── test_rate_limiter.py    # Unit tests
│   └── conftest.py              # Test configuration
├── Dockerfile                   # Container definition
├── docker-compose.yml          # Development environment
├── requirements.txt             # Dependencies
├── .env.example                 # Environment configuration example
└── README.md                    # This file
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest -v tests/

# Run specific test file
python -m pytest tests/test_rate_limiter.py
```

### Test Coverage

Tests include:
- Sliding window algorithm accuracy
- Rate limit enforcement
- Redis integration
- Endpoint discovery
- Response codes and headers

## Deployment

### Docker Deployment

```bash
# Build and start services
docker-compose up --build

# Scale the service
docker-compose up -d --scale app=3
```

### Docker Compose Configuration

```yaml
version: '3.8'
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
  
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
    restart: unless-stopped
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

## Configuration

The library can be configured via environment variables:

| Variable | Description | Default |
|----------|-------------|----------|
| `REDIS_HOST` | Redis server host | `localhost` |
| `REDIS_PORT` | Redis server port | `6379` |
| `REDIS_DB` | Redis database number | `0` |
| `RATE_LIMIT` | Requests per window | `100` |
| `RATE_WINDOW` | Window size in seconds | `60` |

## Monitoring

Rate-limited requests are logged in the following format:
```
[RateLimiter] IP: 127.0.0.1, Timestamp: 2023-01-01 12:00:00, Limit: 100 requests/minute
```