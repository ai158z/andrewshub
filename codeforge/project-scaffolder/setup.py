from setuptools import setup, find_packages
import os
from typing import List

def get_version() -> str:
    """Get the version from the version file or environment variable."""
    return os.environ.get("PROJECT_SCAFFOLDER_VERSION", "0.1.0")

def get_long_description() -> str:
    """Read the README file for long description."""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as fh:
            return fh.read()
    return "Project Scaffolder - A CLI tool for generating project templates"

def get_install_requires() -> List[str]:
    """Get the list of dependencies."""
    return [
        "typer>=0.4.0",
        "pydantic>=1.8.0",
        "cookiecutter>=1.7.0",
        "jinja2>=3.0.0",
    ]

def get_extras_require() -> dict:
    """Get the list of extra dependencies."""
    return {
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.0",
            "mypy>=0.800",
            "flake8>=3.8.0",
        ]
    }

# Only run setup() when this file is executed as a script, not when imported
if __name__ == "__main__":
    setup(
        name="project-scaffolder",
        version=get_version(),
        author="Project Scaffolder Team",
        author_email="scaffolder@example.com",
        description="A CLI tool for generating project templates",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        url="https://github.com/project-scaffolder/scaffolder",
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
        python_requires=">=3.8",
        install_requires=get_install_requires(),
        extras_require=get_extras_require(),
        entry_points={
            "console_scripts": [
                "scaffolder=src.main:main",
            ],
        },
        include_package_data=True,
    )