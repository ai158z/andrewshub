# Project Scaffolding Tool

## Description

A command-line tool for generating project scaffolding for multiple programming languages (Python, JavaScript, Rust) with support for popular frameworks. This tool automates the creation of directory structures, dependency files, and boilerplate code for new projects.

## Features

- Generate project scaffolding for Python, JavaScript (Node.js), and Rust projects
- Framework support for Express (JavaScript), Actix (Rust), and Flask (Python)
- Template-based generation of project files and directory structures
- Interactive CLI interface for project type selection
- Automatic generation of README files with setup instructions
- Docker support for consistent development environments

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- Docker and Docker Compose (optional, for containerization)
- 2GB+ RAM recommended
- Internet connection for package installation

## Installation

```bash
# Clone the repository
git clone <repository-url>

# Change to project directory
cd project-scaffolding-tool

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install .

# OR use via command line
python src/main.py [command] [options]
```

## Environment Variables

The following environment variables can be configured in the `.env` file:

| Variable | Description | Required | Default |
|----------|-------------|-----------|----------|
| `PROJECT_TYPE` | Language/framework type | No | python |
| `OUTPUT_DIR` | Directory to generate files | No | ./projects |

Example `.env` configuration:
```
PROJECT_TYPE=python
OUTPUT_DIR=./projects
```

## Usage

```bash
# Install the tool
pip install project-scaffolding-tool

# Run the tool
project-scaffolding-tool
```

## API Documentation

This tool generates a complete project structure including:
- A `package.json` (for JavaScript) | `requirements.txt` (for Python) | `Cargo.toml` (for Rust) file
- Directory structure (src, tests, etc.)
- Main application file (`main.py`, `index.js`, or `lib.rs`)
- Framework-specific files for Express, Actix, and Flask
- README documentation with project details

## Project Structure

```
project-scaffolding-tool/
├── src/
│   ├── main.py
│   ├── cli.py
│   ├── generator.py
│   ├── templates/
│   │   ├── python_template.py
│   │   ├── javascript_template.py
│   └── rust_template.py
├── tests/
│   └── test_generator.py
├── requirements.txt
├── README.md
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── src/
    └── main.py
```

## Testing

To run the tests for the project, simply execute:
```bash
python -m pytest tests/
```

## Deployment

### Docker

To build and run the tool using Docker:

```bash
# Build the image
docker build -t project-scaffolding-tool .

# Run the container
docker run -it project-scaffolding-tool
```

Make sure to mount the project directory as a volume:
```bash
docker run -it -v $(pwd):/app project-scaffolding-tool
```

### Deployment to Production

To deploy the tool to a production environment, use the generated Docker image:
```bash
# Build the Docker image
docker build -t project-scaffolding-tool . 

# Run the container
docker run -d -p 3000:3000 project-scaffolding-tool
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.