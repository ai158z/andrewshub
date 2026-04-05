from setuptools import setup, find_packages
import os

# Read the contents of README.md
def read_readme():
    """Read the README file for the long description."""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

setup(
    name="json-to-csv-converter",
    version="1.0.0",
    author="",
    author_email="",
    description="A CLI tool to convert JSON files to CSV format with schema validation and blockchain parsing capabilities",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="",
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
        "pandas>=1.3.0",
        "click>=8.0.0",
        "jsonschema>=4.0.0",
        "web3>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "json-to-csv=json_to_csv.cli:main",
        ],
    },
    package_data={
        "": ["*.json", "*.yaml", "*.yml"],
    },
    include_package_data=True,
)