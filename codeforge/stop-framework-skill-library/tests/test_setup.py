import os
import sys
import tempfile
import pytest
from setuptools import __version__, find_packages
from stop_skill_library.setup import setup

def test_setup_name():
    # Test that the package name is set correctly
    assert setup.name == "stop-framework-skill-library"

def test_setup_version():
    # Test that the version is set correctly
    assert setup.version == "0.1.0"

def test_python_requires():
    # Test that python version is properly required
    assert setup.python_requires == ">=3.8"

def test_author_info():
    # Test authors are set correctly
    assert setup.author == "STOP Framework Team"
    assert setup.author_email == "stop-framework@example.com"

def test_description_exists():
    # Test that long description content is set
    assert hasattr(setup, 'description')

def test_long_description_content_type():
    # Test that the long description content type is set
    assert setup.long_description_content_type == "text/markdown"

def test_long_description_fallback():
    # Test long description fallback
    assert "STOP Framework Skill Library" in setup.long_description

def test_package_data():
    # Test package data is included
    package_data = {'stop_skill_library': ['py.typed']}
    assert setup.package_data == package_data

def test_entry_points():
    # Test that entry points are set
    assert 'stop-skill=stop_skill_library.cli:main' in setup.entry_points.values()

def test_install_requires():
    # Test that all required packages are included
    expected_requires = [
        "pydantic>=2.0.0",
        "sqlalchemy>=2.0.0",
        "alembic>=1.10.0",
        "cryptography>=3.0.0",
        "pyyaml>=6.0",
        "jsonschema>=4.0.0"
    ]
    for req in setup.install_requires:
        assert req in expected_requires

def test_classifiers():
    # Test that the classifiers are set correctly
    expected_classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ]
    for classifier in expected_classifiers:
        assert classifier in setup.classifiers

def test_find_packages():
    # Test that find_packages returns the correct packages
    packages = find_packages(exclude=["tests", "examples"])
    assert 'stop_skill_library' in packages

def test_url():
    # Test that the URL is set correctly
    assert setup.url == "https://github.com/stop-framework/sskill-library"

if __name__ == "__main__":
    pytest.main()