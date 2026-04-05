# Staking Reward Calculator

A command-line tool to calculate staking rewards by connecting to the blockchain for live reward rates, calculating potential earnings, and providing historical data visualization.

## Features

- **Live Reward Rates**: Fetches real-time staking reward rates from multiple blockchain networks.
- **Historical Data Visualization**: Provides visualizations of historical staking performance.
- **Flexible Input**: Supports various staking parameters like amount, duration, and network selection.
- **Type-Safe Codebase**: Fully typed Python with Pydantic models for data validation.
- **Docker Support**: Containerized environment for easy setup and execution.

## Prerequisites

- Python 3.9+
- Docker (optional but recommended)
- Access to a blockchain node or API endpoint

## Installation

### Using pip

```bash
pip install -r requirements.txt
```

### Using Docker

```bash
docker build -t staking-reward-calculator .
```

Or using Docker Compose:

```bash
docker-compose up --build
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
BLOCKCHAIN_NODE_URL=https://your-blockchain-node.com
API_ENDPOINT=https://api.example.com
```

## Usage

### CLI

```bash
python src/main.py --amount 1000 --duration 365 --network ethereum
```

### Arguments

| Argument     | Description                      |
### Example

```bash
python src/main.py --amount 1000 --duration 365 --network ethereum
```

## API Documentation

This project does not expose a public API. All interactions are done via the CLI.

## Project Structure

```
staking-reward-calculator/
├── src/
│   ├── main.py
│   ├── staking_calculator.py
│   ├── blockchain_client.py
│   ├── data_fetcher.py
│   ├── validator.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── stake_data.py
│   │   └── reward_rate.py
│   └── utils.py
├── tests/
│   ├── test_staking_calculator.py
│   ├── test_blockchain_client.py
│   ├── test_data_fetcher.py
│   ├── test_validator.py
│   └── conftest.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Testing

Run tests using pytest:

```bash
pytest tests/
```

## Deployment

### With Docker

1. Build the image:

```bash
docker build -t staking-reward-calculator .
```

2. Run the container:

```bash
docker run staking-reward-calculator --amount 1000 --duration 365 --network ethereum
```

### With Docker Compose

1. Start services:

```bash
docker-compose up
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.