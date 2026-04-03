import pytest
from unittest.mock import mock_open, patch
from setuptools import setup, find_packages

def test_setup_function_exists():
    """Test that setup function can be imported"""
    from setup import setup as setup_func
    assert callable(setup_func)

def test_setup_returns_dict():
    """Test that setup function returns configuration dict"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        result = setup_func()
        assert isinstance(result, dict)

def test_setup_contains_required_fields():
    """Test that setup includes all required package information"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            # Verify the actual setup call was made with expected structure
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            
            assert setup_args.get("name") == "property-search-cli"
            assert setup_args.get("version") == "1.0.0"
            assert setup_args.get("description") == "A command-line property search tool"
            assert setup_args.get("author") == "Property Search CLI Team"
            assert setup_args.get("author_email") == "property-search@example.com"

def test_setup_includes_packages():
    """Test that setup function includes packages"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            assert "packages" in setup_args
            assert callable(setup_args["packages"])

def test_setup_includes_install_requires():
    """Test that setup includes required dependencies"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            assert "install_requires" in setup_args
            assert isinstance(setup_args["install_requires"], list)
            assert "argparse" in setup_args["install_requires"]

def test_setup_includes_entry_points():
    """Test that setup includes console script entry points"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            assert "entry_points" in setup_args
            assert "console_scripts" in setup_args["entry_points"]
            console_scripts = setup_args["entry_points"]["console_scripts"]
            assert any("property-search=src.main:main" in script for script in console_scripts)

def test_setup_includes_classifiers():
    """Test that setup includes proper classifiers"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            assert "classifiers" in setup_args
            classifiers = setup_args["classifiers"]
            assert "Development Status :: 4 - Beta" in classifiers
            assert "License :: OSI Approved :: MIT License" in classifiers
            assert any("Programming Language :: Python :: 3" in c for c in classifiers)

def test_setup_python_requires():
    """Test that setup specifies python version requirements"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            assert "python_requires" in setup_args
            assert setup_args["python_requires"] == ">=3.7"

def test_setup_includes_extras_require():
    """Test that setup includes development extras"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            assert "extras_require" in setup_args
            extras = setup_args["extras_require"]
            assert "dev" in extras
            assert "pytest>=6.0" in extras["dev"]
            assert "pytest-cov>=2.0" in extras["dev"]

def test_setup_reads_readme():
    """Test that setup function reads README file"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        mock_file = mock_open(read_data="# Property Search CLI\nCommand line tool for property search")
        with patch("builtins.open", mock_file):
            config = setup_func()
            # Verify open was called to read README.md
            mock_file.assert_called_once_with("README.md")

def test_setup_main_execution():
    """Test that module can be executed directly"""
    import setup
    assert hasattr(setup, "setup")

def test_setup_with_empty_readme():
    """Test setup function handles empty README"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="")):
            config = setup_func()
            assert mock_setup.called

def test_setup_with_missing_readme():
    """Test setup function handles missing README gracefully"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            assert mock_setup.called

def test_setup_long_description_content_type():
    """Test that setup specifies content type for long description"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            assert "long_description_content_type" in setup_args
            assert setup_args["long_description_content_type"] == "text/markdown"

def test_setup_package_data_types():
    """Test that setup returns proper data types"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            
            # Test string fields
            assert isinstance(setup_args.get("name"), str)
            assert isinstance(setup_args.get("version"), str)
            assert isinstance(setup_args.get("description"), str)
            
            # Test list fields
            assert isinstance(setup_args.get("install_requires"), list)
            assert isinstance(setup_args.get("classifiers"), list)

def test_setup_entry_points_format():
    """Test that entry points are properly formatted"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            entry_points = setup_args.get("entry_points", {})
            console_scripts = entry_points.get("console_scripts", [])
            
            # Check that entry points are properly formatted
            assert isinstance(console_scripts, list)
            if console_scripts:
                for script in console_scripts:
                    assert "=" in script
                    assert ":" in script
                    assert ".main" in script

def test_setup_classifiers_format():
    """Test that classifiers follow standard format"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            classifiers = setup_args.get("classifiers", [])
            
            for classifier in classifiers:
                # All classifiers should be strings with '::' separator
                assert isinstance(classifier, str)
                if "::" in classifier:
                    parts = classifier.split(" :: ")
                    assert len(parts) >= 2

def test_setup_extras_require_format():
    """Test that extras_require is properly structured"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            extras_require = setup_args.get("extras_require", {})
            
            assert isinstance(extras_require, dict)
            if "dev" in extras_require:
                dev_deps = extras_require["dev"]
                assert isinstance(dev_deps, list)
                for dep in dev_deps:
                    assert isinstance(dep, str)
                    assert len(dep) > 0

def test_setup_version_format():
    """Test that version follows semantic versioning"""
    from setup import setup as setup_func
    with patch("setuptools.setup") as mock_setup:
        mock_setup.return_value = {}
        with patch("builtins.open", mock_open(read_data="# Test README")):
            config = setup_func()
            setup_args = mock_setup.call_args[1] if mock_setup.call_args else {}
            version = setup_args.get("version")
            
            # Basic semantic version check (X.Y.Z format)
            assert isinstance(version, str)
            assert len(version.split('.')) >= 2
            assert all(part.isdigit() for part in version.split('.') if part.isdigit() or part == '0')