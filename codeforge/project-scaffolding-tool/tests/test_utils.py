import os
import logging
from unittest.mock import patch, mock_open
import pytest
from src.utils import create_directory, write_file, render_template


def test_create_directory_success():
    with patch('os.path.exists') as mock_exists, patch('os.makedirs') as mock_makedirs:
        mock_exists.return_value = False
        create_directory('/test/path')
        mock_makedirs.assert_called_once_with('/test/path', exist_ok=True)


def test_create_directory_already_exists():
    with patch('os.path.exists') as mock_exists, patch('os.makedirs') as mock_makedirs:
        mock_exists.return_value = True
        create_directory('/existing/path')
        mock_makedirs.assert_not_called()


def test_create_directory_raises_os_error():
    with patch('os.path.exists'), patch('os.makedirs', side_effect=OSError("Permission denied")):
        with pytest.raises(OSError):
            create_directory('/test/path')


def test_write_file_success():
    with patch('os.path.exists'), patch('os.makedirs'), patch('builtins.open', mock_open()) as mock_file:
        write_file('/test/file.txt', 'content')
        mock_file().write.assert_called_once_with('content')


def test_write_file_creates_directory():
    with patch('os.path.exists', return_value=False), patch('os.makedirs') as mock_makedirs, \
         patch('builtins.open', mock_open()):
        write_file('/path/to/file.txt', 'content')
        mock_makedirs.assert_called_once_with('/path/to', exist_ok=True)


def test_write_file_io_error():
    with patch('os.path.exists'), patch('os.makedirs'), patch('builtins.open', side_effect=IOError("Write failed")):
        with pytest.raises(IOError):
            write_file('/test/file.txt', 'content')


def test_render_template_success():
    template = "Hello {{ name }}!"
    context = {"name": "World"}
    result = render_template(template, context)
    assert result == "Hello World!"


def test_render_template_missing_context_key():
    template = "Hello {{ name }}!"
    context = {}
    result = render_template(template, context)
    assert result == "Hello !"


def test_render_template_exception():
    with patch('src.utils.Environment.from_string', side_effect=Exception("Template error")):
        with pytest.raises(Exception):
            render_template("{{ name }}", {"name": "test"})


def test_write_file_empty_directory_path():
    with patch('os.path.dirname', return_value=''), patch('builtins.open', mock_open()) as mock_file:
        write_file('file.txt', 'content')
        mock_file().write.assert_called_once_with('content')


def test_write_file_with_nested_path():
    with patch('os.path.exists'), patch('os.makedirs'), patch('builtins.open', mock_open()) as mock_file:
        write_file('dir1/dir2/file.txt', 'content')
        mock_file().write.assert_called_once_with('content')


def test_create_directory_with_none_path():
    with pytest.raises(TypeError):
        create_directory(None)


def test_write_file_none_file_path():
    with pytest.raises(TypeError):
        write_file(None, 'content')


def test_write_file_none_content():
    with patch('os.path.exists'), patch('os.makedirs'), patch('builtins.open', mock_open()) as mock_file:
        write_file('/test/file.txt', None)
        mock_file().write.assert_called_once_with(None)


def test_render_template_none_template():
    with pytest.raises(Exception):
        render_template(None, {})


def test_render_template_none_context():
    result = render_template("test {{ key }}", None)
    assert result == "test "


def test_render_template_empty_context():
    result = render_template("test {{ key }}", {})
    assert result == "test "


def test_render_template_complex_template():
    template = "Items: {% for item in items %}{{ item }},{% endfor %}"
    context = {"items": ["a", "b", "c"]}
    result = render_template(template, context)
    assert result == "Items: a,b,c"


def test_create_directory_empty_string():
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = False
        create_directory('')
        mock_exists.assert_called_once_with('')


def test_write_file_empty_content():
    with patch('os.path.exists'), patch('os.makedirs'), patch('builtins.open', mock_open()) as mock_file:
        write_file('/test/file.txt', '')
        mock_file().write.assert_called_once_with('')