# Wallet Backup Rotation System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An automated wallet backup rotation system that securely backs up wallet data with encryption, maintains retention policies, and integrates with MoonPay wallet APIs.

## Features

- 🔐 **Encrypted Backups**: All wallet data is encrypted before storage using Fernet encryption
- 🗃️ **Retention Policy**: Maintains 7 daily backups and 3 monthly backups with automatic pruning
- ⏰ **Automated Scheduling**: Configurable backup schedules using cron-like syntax
- 🔁 **Automatic Rotation**: Smart backup rotation ensuring efficient storage usage
- 🔄 **Restore Functionality**: Easy restore of wallet data from encrypted backups
- 🌙 **MoonPay Integration**: Direct integration with MoonPay wallet APIs for data fetching
- 🐳 **Container Ready**: Docker support for easy deployment and isolation

## Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)
- MoonPay API credentials

## Installation

### Local Installation

```bash
# Clone the repository
git clone https://github.com/your-username/wallet-backup-rotation.git
cd wallet-backup-rotation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Docker Installation

```bash
# Build the Docker image
docker build -t wallet-backup-rotation .

# Or use docker-compose
docker-compose up --build
```

## Environment Variables

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Required environment variables:

```env
MOONPAY_API_KEY=your_moonpay_api_key_here
ENCRYPTION_KEY=your_32_byte_encryption_key_here
BACKUP_STORAGE_PATH=/path/to/backup/storage
BACKUP_SCHEDULE="0 2 * * *"  # Daily at 2 AM
```

## Usage

### Command Line Interface

```bash
# Create a backup immediately
python -m wallet_backup.cli backup

# Restore from latest backup
python -m wallet_backup.cli restore --latest

# Restore from specific backup
python -m wallet_backup.cli restore --backup-id backup_20240115

# Schedule automated backups
python -m wallet_backup.cli schedule --cron "0 2 * * *"

# List existing backups
python -m wallet_backup.cli list

# Show backup status
python -m wallet_backup.cli status
```

### Programmatic Usage

```python
from wallet_backup.backup_manager import BackupManager
from wallet_backup.moonpay_client import MoonPayClient

# Initialize components
client = MoonPayClient(api_key="your_api_key")
backup_manager = BackupManager(client, storage_path="/backups")

# Create backup
backup_manager.create_backup()

# Restore from backup
backup_manager.restore_backup("backup_20240115")
```

## Project Structure

```
wallet-backup-rotation/
├── src/
│   └── wallet_backup/
│       ├── cli.py          # Command line interface
│       ├── backup_manager.py # Core backup logic
│       ├── encryption.py     # Encryption/decryption utilities
│       ├── storage.py       # Storage management
│       ├── scheduler.py       # Backup scheduling
│       ├── moonpay_client.py # MoonPay API client
│       ├── config.py        # Configuration management
│       └── utils.py        # Utility functions
├── tests/                  # Unit tests
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── requirements.txt          # Python dependencies
├── .env.example            # Environment variable example
└── README.md              # This file
```

## API Documentation

### BackupManager
```python
class BackupManager:
    def create_backup(self) -> str
    def restore_backup(self, backup_id: str) -> bool
    def list_backups(self) -> List[str]
    def prune_old_backups(self) -> None
```

### MoonPayClient
```python
class MoonPayClient:
    def get_wallet_data(self) -> dict
    def validate_credentials(self) -> bool
```

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test module
python -m pytest tests/test_backup_manager.py -v

# Run tests with coverage
python -m pytest --cov=wallet_backup tests/
```

## Deployment

### Docker Deployment

```bash
# Build and run with Docker
docker build -t wallet-backup-rotation .
docker run -d --name wallet-backup wallet-backup-rotation

# Or use docker-compose
docker-compose up -d
```

### Systemd Service (Linux)

Create `/etc/systemd/system/wallet-backup.service`:

```ini
[Unit]
Description=Wallet Backup Rotation Service
After=network.target

[Service]
Type=oneshot
WorkingDirectory=/opt/wallet-backup-rotation
ExecStart=/opt/wallet-backup-rotation/venv/bin/python -m wallet_backup.cli backup
Environment=MOONPAY_API_KEY=your_key_here
Environment=ENCRYPTION_KEY=your_encryption_key_here

[Install]
WantedBy=multi-user.target
```

Add to crontab for scheduling:
```bash
# Run daily at 2 AM
0 2 * * * /opt/wallet-backup-rotation/venv/bin/python -m wallet_backup.cli backup
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