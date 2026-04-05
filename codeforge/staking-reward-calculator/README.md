# Staking Reward Calculator

A fullstack Python-based staking reward calculator with Flask web interface that calculates compound interest rewards for cryptocurrency staking with interactive visualizations.

## Features

- **Compound Interest Calculation**: Implements A = P(1 + r)^t formula for staking rewards
- **Responsive Web Interface**: User-friendly HTML form for inputting staking parameters
- **Data Visualization**: Chart.js integration for reward growth visualization
- **REST API**: Programmatic access to calculation endpoints
- **Mock Data Support**: Fallback demonstration data when no real data available
- **Comprehensive Testing**: Unit tests for calculations and API endpoints
- **Documentation**: Complete setup and usage instructions

## Prerequisites

- Python 3.8+
- pip package manager
- Virtual environment (recommended)

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/staking-reward-calculator.git
cd staking-reward-calculator

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask

# Or install from requirements.txt
pip install -r requirements.txt
```

## Project Setup

```bash
# Set up environment variables (if needed)
# Create .env file in project root
echo "FLASK_ENV=development" > .env
```

## Usage

### Web Interface

Start the Flask application:

```bash
python src/app.py
```

Access the application at `http://localhost:5000`

### API Endpoints

```bash
# Calculate staking rewards
POST /api/calculate
Content-Type: application/json

{
    "stake_amount": 1000,
    "apr": 0.08,
    "duration": 365
}
```

### Example API Response

```json
{
    "input": {
        "stake_amount": 1000,
        "apr": 0.08,
        "duration": 365
    },
    "reward": 80.0,
    "total_value": 1080.0
}
```

## Project Structure

```
staking-reward-calculator/
├── src/
│   ├── app.py                 # Flask application entry point
│   ├── calculator.py          # Compound interest calculation logic
│   ├── routes/
│   │   ├── api.py           # API route handlers
│   │   └── web.py          # Web interface routes
│   └── tests/
│       ├── test_calculator.py        # Unit tests for calculations
│       └── test_api_endpoints.py   # Unit tests for API endpoints
├── static/
│   └── chart.js            # Chart.js library
├── templates/                # HTML templates
├── requirements.txt          # Python dependencies
└── README.md              # Project documentation
```

## API Documentation

### GET `/`

Returns the web interface for staking calculator

### POST `/api/calculate`

Calculate staking rewards

**Request Body:**
```json
{
    "stake_amount": number,
    "apr": number,
    "duration": number
}
```

**Response:**
```json
{
    "input": {
        "stake_amount": number,
        "apr": number,
        "duration": number
    },
    "reward": number,
    "total_value": number
}
```

## Testing

```bash
# Run all tests
python -m pytest src/tests/

# Run specific test file
python -m pytest src/tests/test_calculator.py

# Run with coverage
python -m pytest --cov=src src/tests/
```

## Deployment

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "src/app.py"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  staking-calculator:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `FLASK_DEBUG` | Debug mode | `False` |

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