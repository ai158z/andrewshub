# Skill Library Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A modular skill library framework with curiosity-driven task scoring and predictive modeling capabilities. Built with Python, FastAPI, and PyTorch.

## Features

- **Modular Architecture**: Categorize skills by domain, complexity, and utility
- **Predictive Scoring**: AI-powered task relevance, novelty, and resource requirement scoring
- **Vector Similarity**: FAISS-based skill matching and similarity search
- **Curiosity Budget**: Dynamic allocation of learning resources based on novelty
- **Memory Integration**: Continuous learning through memory system integration
- **RESTful API**: FastAPI-powered endpoints for skill and task management

## Prerequisites

- Python 3.8+
- Docker & Docker Compose (for development)
- PostgreSQL
- Redis

## Installation

### Using Docker Compose (Recommended for Development)

```bash
# Clone the repository
git clone <repository-url>
cd skill-library-framework

# Copy and configure environment variables
cp .env.example .env
# Edit .env file with your configurations

# Build and start services
docker-compose up --build
```

### Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn src.skill_library.api.main:app --reload
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/skill_db
REDIS_URL=redis://localhost:6379/0
DEBUG=True
SECRET_KEY=your-secret-key
```

## Usage Examples

### Starting the Service

```bash
# Using Docker
docker-compose up

# Using uvicorn directly
uvicorn src.skill_library.api.main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

- `GET /skills/` - List all skills
- `POST /skills/` - Create new skill
- `GET /skills/{skill_id}` - Get skill details
- `POST /tasks/score` - Score a task based on skills
- `GET /predict` - Get skill predictions

## API Documentation

Once the server is running, API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
skill-library-framework/
├── src/
│   └── skill_library/
│       ├── __init__.py
│       ├── core/           # Core skill framework
│       ├── models/         # ML models and scoring
│       ├── storage/         # Database and repository layer
│       ├── integrations/    # External system integrations
│       └── api/           # FastAPI endpoints
├── tests/                  # Unit and integration tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test modules
python -m pytest tests/test_skill_framework.py
python -m pytest tests/test_predictive_model.py
python -m pytest tests/test_curiosity_budget.py
```

## Deployment

### Docker Deployment

```bash
# Build and push to registry
docker build -t skill-library-framework .
docker push skill-library-framework:latest

# Run in production
docker run -d -p 8000:8000 skill-library-framework
```

### Environment Configuration

Production `.env`:
```env
DATABASE_URL=postgresql://prod:5432/db
REDIS_URL=redis://prod-redis:6379
DEBUG=False
WORKERS=4
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## Acknowledgments

- Built with FastAPI for high-performance API handling
- Machine learning powered by PyTorch
- Vector similarity using FAISS
- Dockerized for easy deployment and scaling