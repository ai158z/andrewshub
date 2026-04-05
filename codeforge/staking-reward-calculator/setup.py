from setuptools import setup, find_packages

# Read the contents of README file
from pathlib import Path
this_directory = Path(__file__).parent
readme = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""
if not readme:
    readme = (this_directory / "README.rst").read_text() if (this_directory / "README.rst").exists() else ""

setup(
    name="staking-reward-calculator",
    version="1.0.0",
    author="Staking Rewards Team",
    author_email="contact@stakingrewards.example",
    description="A CLI tool for calculating staking rewards across different blockchain networks",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/staking-rewards/calculator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
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
    install_requires=[
        "click>=8.0.0",
        "matplotlib>=3.5.0",
        "pandas>=1.4.0",
        "requests>=2.28.0",
        "numpy>=1.21.0",
    ],
    entry_points={
        "console_scripts": [
            "staking-calculator = staking_calculator.cli:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
        ]
    },
    package_data={
        "staking_calculator": ["*.json", "data/*.json"],
    },
    include_package_data=True,
)