# Staking Reward Calculator

A fullstack web application for calculating staking rewards with real-time network data integration, time-based projections, and ROS2 sensor compatibility.

## Features

- **Staking Calculations**: Real-time staking reward calculations with customizable parameters
- **Network Data Integration**: Live blockchain network statistics and data
- **Time-based Projections**: Future reward projections with visual charts
- **ROS2 Compatibility**: Integration with ROS2 sensor data for enhanced functionality
- **Real-time Price Data**: Cryptocurrency price oracle integration
- **Responsive UI**: Modern React frontend with interactive visualizations

## Prerequisites

- Python 3.8+
- Node.js 14+
- Docker and Docker Compose (for containerized deployment)
- Redis server (included in Docker setup)

## Installation

### Backend Setup

```bash
# Clone the repository
git clone <repository-url>
cd staking-reward-calculator

# Install Python dependencies
pip install -r backend/requirements.txt

# Install Node.js dependencies
cd frontend
npm install
```

### Environment Variables

Create a `.env` file based on `backend/.env.example`:

```env
# Database
DATABASE_URL=sqlite:///./test.db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# API Keys
BLOCKCHAIN_API_KEY=your_api_key_here
PRICE_ORACLE_API_KEY=your_price_api_key_here

# ROS2 Settings
ROS2_ENABLED=false
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Development
npm start

# Production build
npm run build
```

## Project Structure

```
staking-reward-calculator/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── api/
    │   └── App.js
    └── package.json
```

## Usage

### Running with Docker Compose

```bash
# Start all services
cd backend
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### API Endpoints

#### Staking Calculations
```
POST /api/calculator/rewards
```
Calculate staking rewards based on input parameters.

#### Network Data
```
GET /api/network/stats
GET /api/network/validators
```

#### Projections
```
GET /api/projections/future
GET /api/projections/historical
```

## API Documentation

### Example Request
```bash
curl -X POST "http://localhost:8000/api/calculator/rewards" \
  -H "Content-Type: application/json" \
  -d '{
    "stake_amount": 1000,
    "duration_days": 365,
    "compound_frequency": "daily"
  }'
```

### Response
```json
{
  "total_rewards": 150.50,
  "apy": 15.5,
  "projected_rewards": [
    {"day": 30, "reward": 12.25},
    {"day": 60, "reward": 25.75}
  ]
}
```

## Testing

```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm test

# Integration tests
npm run test:integration
```

## Deployment

### Production Deployment

1. **Build Docker Images**
```bash
# Backend
cd backend
docker build -t staking-calculator-backend .

# Frontend
cd frontend
npm run build
```

2. **Environment Configuration**
```bash
# Set production environment variables
export NODE_ENV=production
export PORT=8080
```

3. **Docker Compose for Production**
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - NODE_ENV=production
    depends_on:
      - redis

  frontend:
    build: ./frontend
    ports:
      - "80:80"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Staking Reward Calculator

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