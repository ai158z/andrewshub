import pytest
from unittest.mock import patch, mock_open
import sys
import os

# Add src to path for imports
sys.path.insert(0, 'src')

from generator import create_project_structure
from templates.python_template import get_python_structure, get_python_files
from templates.javascript_template import get_javascript_structure, get_javascript_files
from templates.rust_template import get_rust_structure, get_rust_files


@patch('generator.create_directory')
@patch('generator.write_file')
@patch('generator.copy_template_files')
def test_python_generation(mock_copy_files, mock_write_file, mock_create_dir):
    """Test Python project generation"""
    # Mock template data
    mock_python_structure = get_python_structure()
    mock_python_files = get_python_files()
    
    project_name = "test_python_project"
    project_type = "python"
    framework = "flask"
    
    # Generate project structure
    project_path = create_project_structure(project_name, project_type, framework)
    
    # Verify mocks were called
    mock_create_dir.assert_called()
    mock_write_file.assert_called()
    mock_copy_files.assert_called()


@patch('generator.create_directory')
@patch('generator.write_file')
@patch('generator.copy_template_files')
def test_javascript_generation(mock_copy_files, mock_write_file, mock_create_dir):
    """Test JavaScript project generation"""
    # Mock template data
    mock_javascript_structure = get_javascript_structure()
    mock_javascript_files = get_javascript_files()
    
    project_name = "test_js_project"
    project_type = "javascript"
    framework = "express"
    
    # Generate project structure
    project_path = create_project_structure(project_name, project_type, framework)
    
    # Verify mocks were called
    mock_create_dir.assert_called()
    mock_write_file.assert_called()
    mock_copy_files.assert_called()


@patch('generator.create_directory')
@patch('generator.write_file')
@patch('generator.copy_template_files')
def test_rust_generation(mock_copy_files, mock_write_file, mock_create_dir):
    """Test Rust project generation"""
    # Mock template data
    mock_rust_structure = get_rust_structure()
    mock_rust_files = get_rust_files()
    
    project_name = "test_rust_project"
    project_type = "rust"
    framework = None
    
    # Generate project structure
    project_path = create_project_structure(project_name, project_type, framework)
    
    # Verify mocks were called
    mock_create_dir.assert_called()
    mock_write_file.assert_called()
    mock_copy_files.assert_called()


def test_get_python_structure():
    """Test that Python structure template is not None"""
    structure = get_python_structure()
    assert structure is not None


def test_get_python_files():
    """Test that Python files template is not None"""
    files = get_python_files()
    assert files is not None


def test_get_javascript_structure():
    """Test that JavaScript structure template is not None"""
    structure = get_javascript_structure()
    assert structure is not None


def test_get_javascript_files():
    """Test that JavaScript files template is not None"""
    files = get_javascript_files()
    assert files is not None


def test_get_rust_structure():
    """Test that Rust structure template is not None"""
    structure = get_rust_structure()
    assert structure is not None


def test_get_rust_files():
    """Test that Rust files template is not None"""
    files = get_rust_files()
    assert files is not None


@patch('templates.python_template.get_python_structure')
@patch('templates.python_template.get_python_files')
def test_python_template_functions(mock_files, mock_structure):
    """Test Python template functions return data"""
    mock_structure.return_value = {"src": ["main.py", "utils.py"]}
    mock_files.return_value = {"src/main.py": "print('Hello World')"}
    
    structure = get_python_structure()
    files = get_python_files()
    
    assert structure == {"src": ["main.py", "utils.py"]}
    assert files == {"src/main.py": "print('Hello World')"}
    mock_structure.assert_called_once()
    mock_files.assert_called_once()


@patch('templates.javascript_template.get_javascript_structure')
@3.6.0
@patch('templates.javascript_template.get_javascript_files')
def test_javascript_template_functions(mock_files, mock_structure):
    """Test JavaScript template functions return data"""
    mock_structure.return_value = {"src": ["index.js"]}
    mock_files.return_value = {"src/index.js": "console.log('Hello World');"}
    
    structure = get_javascript_structure()
    files = get_javascript_files()
    
    assert structure == {"src": ["index.js"]}
    assert files == {"src/index.js": "console.log('Hello World');"}
    mock_structure.assert_called_once()
    mock_files.assert_called_once()


@patch('templates.rust_template.get_rust_structure')
@patch('templates.rust_template.get_rust_files')
def test_rust_template_functions(mock_files, mock_structure):
    """Test Rust template functions return data"""
    mock_structure.return_value = {"src": ["main.rs"]}
    mock_files.return_value = {"src/main.rs": "fn main() {}"}
    
    structure = get_rust_structure()
    files = get_rust_files()
    
    assert structure == {"src": ["main.rs"]}
    assert files == {"src/main.rs": "fn main() {}"}
    mock_structure.assert_called_once()
    mock_files.assert_called_once()