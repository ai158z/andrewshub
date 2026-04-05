# Skill Library Predictor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A self-evolving skill library system with predictive task scoring using historical data. This library tracks skill proficiency over time, adjusts curiosity budgets based on success rates, and predicts task outcomes using machine learning.

## Features

- **Skill Proficiency Tracking**: Monitor skills with name, proficiency level, success rate, and last used timestamp
- **Adaptive Curiosity Budget**: Dynamic budget adjustment based on historical success rates
- **Task Outcome Prediction**: Machine learning-based prediction of task success using historical data
- **Self-Evolving Library**: Skills improve automatically based on usage patterns
- **FastAPI Backend**: High-performance REST API with automatic documentation
- **Authentication & Authorization**: Secure API access control
- **Comprehensive Testing**: Full test coverage for all core components

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- Docker (optional, for containerized deployment)

## Installation

### Local Installation

```bash
# Clone the repository
git clone https://github.com/your-username/skill-library-predictor.git
cd skill-library-predictor

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn src.main:app --reload
```

### Docker Installation

```bash
# Build and run with Docker
docker-compose up --build
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | API authentication secret | `your-secret-key` |
| `DATABASE_URL` | Database connection string | `sqlite:///./skills.db` |

## Usage Examples

### API Endpoints

```bash
# Add a new skill
curl -X POST "http://localhost:8000/skills/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Python", "proficiency": 0.8, "success_rate": 0.9}'

# Predict task outcome
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{"task_data": {"skill_id": 1, "complexity": 5}}'

# Get curiosity budget
curl -X GET "http://localhost:8000/curiosity/budget/"
```

## Project Structure

```
skill-library-predictor/
├── src/
│   ├── main.py                 # FastAPI app and routes
│   ├── skill_library.py        # Skill library management
│   ├── task_predictor.py       # Task prediction engine
│   ├── curiosity_budget.py       # Curiosity budget manager
│   ├── skill_proficiency.py    # Skill proficiency tracking
│   ├── task_outcome_predictor.py # Task outcome prediction
│   ├── auth.py                # Authentication system
│   ├── models.py             # Data models
│   └── utils.py             # Utility functions
├── tests/                   # Unit tests
│   ├── test_skill_library.py
│   ├── test_task_predictor.py
│   └── ... (all test files)
├── requirements.txt           # Python dependencies
├── Dockerfile               # Docker configuration
└── docker-compose.yml      # Docker Compose setup
```

## API Documentation

The API automatically generates interactive documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_skill_library.py -v

# Run with coverage
python -m pytest tests/ --cov=src/ --cov-report=html
```

## Deployment

### Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
```

### Production Deployment

```bash
# Build for production
docker build -t skill-library-predictor .

# Run in production
docker run -d -p 8000:8000 skill-library-predictor
```

## Dependencies

See `requirements.txt` for complete dependency list:

- fastapi>=0.68.0
- uvicorn>=0.15.0
- pydantic>=1.8.0
- python-multipart>=0.0.5
- shelved_pca>=0.1.0
- scikit-learn>=1.0.0

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Skill Library Predictor

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