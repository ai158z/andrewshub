# Code Review Analyzer

A CLI tool for automated code review analysis that detects static issues, security vulnerabilities, and style violations in pull requests and code patches.

## Features

- **Multi-source Input**: Analyze GitHub PR URLs or local patch files
- **Comprehensive Analysis**: Combines static analysis, security scanning, and style checking
- **Structured Reporting**: JSON output with findings categorized by severity (low, medium, high)
- **Multiple Checkers**: Integrates pylint, bandit, and flake8 with custom rules
- **Flexible Configuration**: Adjustable rule thresholds and severity levels

## Prerequisites

- Python 3.8+
- pip package manager
- Git (for version control systems access)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/code-review-analyzer.git
cd code-review-analyzer

# Install dependencies
pip install -r requirements.txt
```

## Environment Variables

```bash
# GitHub Personal Access Token (optional, for private repositories)
GITHUB_TOKEN=your_github_token_here
```

## Usage

```bash
# Analyze a GitHub PR
python src/main.py analyze --url https://github.com/user/repo/pull/123

# Analyze a local patch file
python src/main.py analyze --patch ./changes.patch

# Generate verbose output
python src/main.py analyze --url <PR_URL> --verbose

# Specify custom config
python src/main.py analyze --url <PR_URL> --config ./config/custom_rules.json
```

## API Documentation

### CLI Commands

```
Usage: python src/main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  analyze  Analyze code changes for issues
```

### Configuration

The tool uses a JSON configuration file to control:
- Rule severity thresholds
- Enabled/disabled check categories
- Custom rule definitions
- Output formatting options

## Project Structure

```
code-review-analyzer/
├── src/
│   ├── main.py                 # CLI entry point
│   ├── analyzer.py              # Core analysis orchestrator
│   ├── github_client.py        # GitHub API client
│   ├── patch_parser.py         # Unified diff parser
│   ├── rules_engine.py         # Rule application engine
│   ├── report_generator.py      # JSON report creation
│   ├── checks/
│   │   ├── security.py         # Security vulnerability checks
│   │   ├── style.py            # Code style checks
│   │   └── static_analysis.py  # Static analysis checks
│   └── utils/
│       ├── config.py           # Configuration management
│       └── logger.py          # Logging utilities
├── tests/                     # Unit tests
├── requirements.txt             # Python dependencies
└── README.md                 # Documentation
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test module
python -m pytest tests/test_analyzer.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Test Structure

- `test_analyzer.py`: Core analysis logic tests
- `test_github_client.py`: GitHub API integration tests
- `test_patch_parser.py`: Diff parsing logic tests
- `test_report_generator.py`: JSON report generation tests

## Deployment

No specific deployment required - CLI tool runs locally. For Docker deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "src/main.py"]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Code Review Analyzer Contributors

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