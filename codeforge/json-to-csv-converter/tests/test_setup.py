import pytest
from setuptools import setup, find_packages
from unittest.mock import mock_open, patch
import os

@pytest.fixture
def setup_kwargs():
    return {
        "name": "json-to-csv-converter",
        "version": "1.0.0",
        "author": "",
        "author_email": "",
        "description": "A CLI tool to convert JSON files to CSV format with schema validation and blockchain parsing capabilities",
        "long_description_content_type": "text/markdown",
        "url": "",
        "packages": find_packages(where="src"),
        "package_dir": {"": "src"},
        "classifiers": [
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
        "python_requires": ">=3.8",
        "install_requires": [
            "pandas>=1.3.0",
            "click>=8.0.0",
            "jsonschema>=4.0.0",
            "web3>=6.0.0",
        ],
        "entry_points": {
            "console_scripts": [
                "json-to-csv=json_to_csv.cli:main",
            ],
        },
        "package_data": {
            "": ["*.json", "*.yaml", "*.yml"],
        },
        "include_package_data": True,
    }

def test_setup_name(setup_kwargs):
    assert setup_kwargs["name"] == "json-to-csv-converter"

def test_setup_version(setup_kwargs):
    assert setup_kwargs["version"] == "1.0.0"

def test_setup_description(setup_kwargs):
    expected = "A CLI tool to convert JSON files to CSV format with schema validation and blockchain parsing capabilities"
    assert setup_kwargs["description"] == expected

def test_setup_classifiers(setup_kwargs):
    classifiers = setup_kwargs["classifiers"]
    assert "Development Status :: 4 - Beta" in classifiers
    assert "Intended Audience :: Developers" in classifiers
    assert "License :: OSI Approved :: MIT License" in classifiers
    assert "Operating System :: OS Independent" in classifiers
    assert "Programming Language :: Python :: 3.8" in classifiers

def test_setup_python_requires(setup_kwargs):
    assert setup_kwargs["python_requires"] == ">=3.8"

def test_setup_entry_points(setup_kwargs):
    entry_points = setup_kwargs["entry_points"]
    assert "console_scripts" in entry_points
    assert entry_points["console_scripts"][0] == "json-to-csv=json_to_csv.cli:main"

def test_setup_install_requires(setup_kwargs):
    install_requires = setup_kwargs["install_requires"]
    assert "pandas>=1.3.0" in install_requires
    assert "click>=8.0.0" in install_requires
    assert "jsonschema>=4.0.0" in install_requires
    assert "web3>=6.0.0" in install_requires

def test_setup_package_data(setup_kwargs):
    package_data = setup_kwargs["package_data"]
    assert "" in package_data
    assert "*.json" in package_data[""]
    assert "*.yaml" in package_data[""]

def test_setup_include_package_data(setup_kwargs):
    assert setup_kwargs["include_package_data"] is True

def test_setup_packages(setup_kwargs):
    expected_packages = find_packages(where="src")
    assert setup_kwargs["packages"] == expected_packages

def test_setup_package_dir(setup_kwargs):
    assert setup_kwargs["package_dir"] == {"": "src"}

@patch("setuptools.setup")
def test_setup_function_call(mock_setup, setup_kwargs):
    setup(**setup_kwargs)
    mock_setup.assert_not_called()

def test_long_description_file_read(setup_kwargs):
    with patch("builtins.open", mock_open(read_data="test content")) as mock_file:
        content = open("README.md").read()
        mock_file.assert_called_once_with("README.md", "r")

def test_setup_author_empty(setup_kwargs):
    assert setup_kwargs["author"] == ""

def test_setup_author_email_empty(setup_kwargs):
    assert setup_kwargs["author_email"] == ""

def test_setup_url_empty(setup_kwargs):
    assert setup_kwargs["url"] == ""

def test_setup_long_description_type(setup_kwargs):
    assert setup_kwargs["long_description_content_type"] == "text/markdown"

def test_setup_entry_point_structure(setup_kwargs):
    entry_points = setup_kwargs["entry_points"]
    assert "console_scripts" in entry_points
    assert isinstance(entry_points["console_scripts"], list)

def test_setup_entry_point_command(setup_kwargs):
    entry_points = setup_kwargs["entry_points"]
    assert "json-to-csv=json_to_csv.cli:main" in entry_points["console_scripts"]

def test_setup_python_version_support(setup_kwargs):
    classifiers = setup_kwargs["classifiers"]
    python_versions = [c for c in classifiers if "Python ::" in c]
    assert len(python_versions) >= 4
    assert "Programming Language :: Python :: 3.8" in python_versions
    assert "Programming Language :: Python :: 3.9" in python_versions
    assert "Programming Language :: Python :: 3.10" in python_versions
    assert "Programming Language :: Python :: 3.11" in python_versions