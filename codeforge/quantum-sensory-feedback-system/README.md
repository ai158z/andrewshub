# Quantum Sensory Feedback System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A quantum-inspired sensory feedback system that integrates the Orchestrated Objective Reduction (Orch-OR) theoretical framework for adaptive perception in android embodiment systems.

## Features

- **Quantum Processing**: Implements quantum algorithms for sensory data processing
- **Orch-OR Integration**: Applies Penrose-Hameroff quantum consciousness theory to perception modeling
- **Adaptive Perception**: Dynamic adjustment of sensory processing based on environmental feedback
- **Real-time Processing**: Low-latency sensory data handling and response generation
- **Containerized Deployment**: Docker support for easy deployment and scaling

## Prerequisites

- Python 3.8+
- Docker (for containerized deployment)
- Redis server
- RabbitMQ server

## Installation

### Local Setup

```bash
# Clone the repository
git clone https://github.com/your-username/quantum-sensory-feedback-system.git
cd quantum-sensory-feedback-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Docker Setup

```bash
# Build and start services
docker-compose up --build
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
REDIS_HOST=redis
REDIS_PORT=6379
MONGODB_HOST=mongodb://localhost:27017
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
DEBUG=false
PORT=8000
```

## Project Structure

```
quantum-sensory-feedback-system/
├── src/
│   ├── sensory/
│   │   ├── input_handler.py
│   │   ├── quantum_processor.py
│   │   └── orch_or_engine.py
│   ├── perception/
│   │   ├── adaptation.py
│   │   └── pattern_recognition.py
│   ├── feedback/
│   │   ├── actuator.py
│   │   └── response_generator.py
│   ├── models/
│   │   ├── sensory_data.py
│   │   ├── quantum_state.py
│   │   └── perception_model.py
│   └── utils/
│       ├── quantum_math.py
│       └── signal_processing.py
├── main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Usage Examples

### Starting the Server

```bash
# Local development
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

```http
POST /api/sensory/process
Content-Type: application/json

{
  "sensor_data": {
    "type": "tactile",
    "value": 0.75,
    "timestamp": "2023-01-01T12:00:00Z"
  }
}
```

## API Documentation

API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

- `POST /api/sensory/process` - Process sensory input data
- `GET /api/health` - System health check
- `POST /api/quantum/execute` - Execute quantum processing operations

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test suite
python -m pytest tests/test_sensory.py
```

## Deployment with Docker

### Building the Image

```dockerfile
docker build -t quantum-sensory-system .
```

### Docker Compose Services

The system requires the following services:
- **Redis**: Caching and session storage
- **RabbitMQ**: Message queuing
- **MongoDB**: Optional persistent storage

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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