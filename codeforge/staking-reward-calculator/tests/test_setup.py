import pytest
from setuptools import setup
from unittest.mock import patch, mock_open


def test_setup_name():
    """Test that the package name is correct in setup configuration."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            # Import the setup.py to trigger setup call
            with patch("sys.argv", ["setup.py", "check"]):  # Prevent actual setup execution
                exec(open("setup.py").read())
    
    mock_setup.assert_called_once()
    args, kwargs = mock_setup.call_args
    assert kwargs['name'] == "staking-reward-calculator"


def test_setup_version():
    """Test that the version is correctly set in setup configuration."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    assert kwargs['version'] == "0.1.0"


def test_setup_author():
    """Test that the author is correctly set in setup configuration."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    assert kwargs['author'] == "Staking Calculator Team"


def test_setup_author_email():
    """Test that the author email is correctly set in setup configuration."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    assert kwargs['author_email'] == "staking.calculator@example.com"


def test_setup_description():
    """Test that the description is correctly set in setup configuration."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    assert "calculator for staking rewards" in kwargs['description']


def test_setup_long_description_content_type():
    """Test that long description content type is set correctly."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    assert kwargs['long_description_content_type'] == "text/markdown"


def test_setup_url():
    """Test that the URL is correctly set in setup configuration."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    assert kwargs['url'] == "https://github.com/staking-calculator/staking-reward-calculator"


def test_setup_packages():
    """Test that packages are found correctly."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    # We can't directly test find_packages result without importing the actual module
    assert 'packages' in kwargs


def test_setup_package_dir():
    """Test that package directory is correctly set."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    assert kwargs['package_dir'] == {"": "src"}


def test_setup_python_requires():
    """Test that python requirements are correctly set."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    assert kwargs['python_requires'] == ">=3.7"


def test_setup_install_requires():
    """Test that install requirements are correctly set."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    assert "argparse" in kwargs['install_requires']
    assert "decimal" in kwargs['install_requires']


def test_setup_entry_points():
    """Test that entry points are correctly set."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    assert 'console_scripts' in kwargs['entry_points']
    entry_points = kwargs['entry_points']['console_scripts']
    assert any("staking-calculator=cli:main" in ep for ep in entry_points)


def test_setup_extras_require():
    """Test that extras requirements are correctly set."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    assert 'dev' in kwargs['extras_require']
    dev_deps = kwargs['extras_require']['dev']
    assert any("pytest" in dep for dep in dev_deps)
    assert any("pytest-cov" in dep for dep in dev_deps)


def test_setup_classifiers_has_required_categories():
    """Test that required classifiers are present."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    classifiers = kwargs['classifiers']
    assert "License :: OSI Approved :: MIT License" in classifiers
    assert "Programming Language :: Python :: 3" in classifiers
    assert "Operating System :: OS Independent" in classifiers


def test_setup_contains_required_keywords():
    """Test that required keywords are present."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    keywords = kwargs['keywords']
    assert "staking" in keywords
    assert "apy" in keywords
    assert "finance" in keywords


def test_setup_project_urls():
    """Test that project URLs are correctly set."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    project_urls = kwargs['project_urls']
    assert "Bug Reports" in project_urls
    assert "Source" in project_urls
    assert project_urls["Bug Reports"] == "https://github.com/staking-calculator/staking-reward-calculator/issues"
    assert project_urls["Source"] == "https://github.com/staking-calculator/staking-reward-calculator"


def test_setup_contains_finance_classifiers():
    """Test that finance-related classifiers are present."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    classifiers = kwargs['classifiers']
    finance_classifiers = [c for c in classifiers if 'Financial' in c]
    assert len(finance_classifiers) >= 2  # At least 2 finance-related classifiers


def test_setup_contains_python_versions():
    """Test that Python version classifiers are present."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    classifiers = kwargs['classifiers']
    python_classifiers = [c for c in classifiers if c.startswith("Programming Language :: Python :: 3")]
    assert len(python_classifiers) >= 4  # Should have at least 4 Python 3.x version classifiers


def test_setup_has_console_script_entry_points():
    """Test that console script entry points are correctly configured."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    entry_points = kwargs['entry_points']
    # Check that we have console script entry points
    assert 'console_scripts' in entry_points
    console_scripts = entry_points['console_scripts']
    # Check that our staking calculator script is in the entry points
    assert any('staking-calculator' in script for script in console_scripts)


def test_setup_install_requirements_minimum():
    """Test that minimum required dependencies are present."""
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="Test Description")):
            with patch("sys.argv", ["setup.py", "check"]):
                exec(open("setup.py").read())
    
    args, kwargs = mock_setup.call_args
    install_requires = kwargs['install_requires']
    assert "argparse" in install_requires
    assert "decimal" in install_requires