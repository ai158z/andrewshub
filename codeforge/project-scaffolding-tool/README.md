# Project Scaffolding Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line interface tool that automates project setup for common project types (web apps, CLIs, libraries) with directory structure, dependencies, and boilerplate code generation.

## Features

- **CLI Interface**: Interactive command-line interface for project type selection
- **Directory Structure**: Automatic creation of standardized project layouts
- **Dependency Management**: Installs dependencies based on project type
- **Boilerplate Generation**: Pre-configured starter code for multiple languages
- **Documentation**: Automatic README and license file creation
- **Version Control**: Git repository initialization
- **Testing Setup**: Integrated testing framework configuration
- **Containerization**: Dockerfile generation for containerized projects
- **Multi-language Support**: Python, JavaScript (Node.js), and Rust project templates
- **Extensible Architecture**: Modular design for easy language/framework additions

## Prerequisites

- Python 3.8+
- Node.js (for JavaScript projects)
- Cargo (for Rust projects)
- Git

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/project-scaffolding-tool.git
cd project-scaffolding-tool

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Environment Variables

No specific environment variables required for basic usage.

## Usage Examples

```bash
# Run the scaffolding tool
project-scaffolding-tool

# The tool will prompt for:
# - Project name
# - Project type (web app, CLI, library)
# - Programming language
# - Additional features (testing, Docker, etc.)
```

## API Documentation

This is a CLI tool with the following main commands:

### Main Entry Point
```bash
project-scaffolding-tool
```

### Interactive Prompts
The tool will guide you through:
1. Project name selection
2. Project type choice
3. Language selection
4. Feature selection (Git, Testing, Docker)

## Project Structure

```
project-scaffolding-tool/
├── src/
│   └── main.py              # Main entry point
├── scaffolding/
│   ├── config.py             # Configuration module
│   ├── cli.py              # CLI interface
│   ├── generator.py          # File/directory generator
│   └── templates/           # Project templates
│       ├── python.py
│       ├── javascript.py
│       └── rust.py
├── tests/                  # Test files
├── requirements.txt           # Python dependencies
└── setup.py               # Package configuration
```

## Configuration

The tool uses configuration files to determine:
- Default project structures
- Template settings
- Dependency lists
- File generation rules

## Testing

```bash
# Run tests
python -m pytest tests/

# Run tests with coverage
python -m pytest --cov=scaffolding tests/
```

## Deployment

### Docker Deployment

```dockerfile
# Example Dockerfile for the tool
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN pip install -e .

CMD ["project-scaffolding-tool"]
```

### Building Docker Image

```bash
docker build -t project-scaffolding-tool .
docker run -it project-scaffolding-tool
```

## Extending the Tool

The tool is designed with an extensible architecture:

1. **Adding New Languages**: Create new template files in `scaffolding/templates/`
2. **Custom Project Types**: Add new configuration classes
3. **Additional Features**: Extend the generator module

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT License permits use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, subject to the conditions that the copyright notice and permission notice are included in all copies or substantial portions of the software.