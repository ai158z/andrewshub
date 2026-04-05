# Agent Dashboard ROS2

A full-stack agent monitoring dashboard with ROS2 integration for Android embodiment systems. This project provides real-time system health monitoring, agent status tracking, and operational metrics visualization with seamless ROS2 communication.

## Features

- **Real-time System Monitoring**: Track CPU, memory, and network metrics
- **Agent Management**: Monitor and manage distributed agents
- **ROS2 Integration**: Native support for ROS2-based Android embodiment systems
- **Comprehensive Dashboard**: Interactive UI with real-time data visualization
- **RESTful API**: Full-featured API for agent and metric management
- **Database Integration**: PostgreSQL backend with SQLAlchemy ORM

## Prerequisites

- Python 3.8+
- Docker & Docker Compose
- Node.js 14+ (for React frontend)
- ROS2 Foxy/Focal (or later)

## Project Structure

```
agent-dashboard-ros2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── config/
│   └── main.py
├── frontend/
│   ├── src/
│   └── package.json
├── docker-compose.yml
└── requirements.txt
```

## Installation & Setup

### Backend Setup

```bash
# Clone repository
git clone https://github.com/your-username/agent-dashboard-ros2.git
cd agent-dashboard-ros2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend Setup

```bash
# Install frontend dependencies
cd frontend
npm install
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dashboard_db
ROS2_DOMAIN_ID=0
DEBUG=True
```

## Docker Compose Setup

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: agent_dashboard
      POSTGRES_USER: dashboard_user
      POSTGRES_PASSWORD: dashboard_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  ros2:
    image: ros:foxy
    command: ros2 daemon start
    environment:
      - ROS_DOMAIN_ID=0
    network_mode: host

volumes:
  postgres_data:
```

## Usage Examples

### Starting the Application

```bash
# Start backend server
uvicorn backend.app.main:app --reload

# Start frontend development server
cd frontend && npm start
```

### API Endpoints

| Endpoint | Method | Description |
|--------|--------|-------------|
| `/api/agents` | GET | List all agents |
| `/api/agents/{id}` | GET | Get agent details |
| `/api/metrics` | GET | Get system metrics |
| `/api/system/health` | GET | System health status |

## API Documentation

API documentation is available at `/docs` when the server is running.

## Testing

```bash
# Run backend tests
cd backend
python -m pytest tests/

# Run frontend tests
cd frontend
npm test
```

## Deployment

### Docker Deployment

```bash
# Build and start services
docker-compose up -d

# Build project
docker-compose build

# Scale services
docker-compose up --scale web=3
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2023 Your Company

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