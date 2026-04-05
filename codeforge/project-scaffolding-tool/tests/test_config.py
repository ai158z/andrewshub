import json
import os
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import pytest

from src.scaffolding.config import get_project_config, save_config, load_default_config, save_default_config

def test_get_project_config_file_exists_and_valid(tmp_path):
    config_file = tmp_path / ".scaffolding_config.json"
    config_content = {"project_name": "test", "version": "1.0"}
    config_file.write_text(json.dumps(config_content))
    
    with patch('pathlib.Path', return_value=Path(config_file)):
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(config_content))):
                result = get_project_config()
                assert result == config_content

def test_get_project_config_file_not_exists(tmp_path):
    with patch('pathlib.Path.exists', return_value=False):
        result = get_project_config()
        assert result == {}

def test_get_project_config_file_exists_but_invalid(tmp_path):
    config_file = tmp_path / ".scaffolding_config.json"
    config_file.write_text("invalid json")
    
    with patch('pathlib.Path', return_value=Path(config_file)):
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data="invalid json")):
                result = get_project_config()
                assert result == {}

def test_get_project_config_file_read_error():
    with patch('pathlib.Path.exists', return_value=True):
        with patch('builtins.open', side_effect=Exception("File read error")):
            result = get_project_config()
            assert result == {}

def test_save_config_success():
    config_data = {"project_name": "test", "version": "1.0"}
    with patch('builtins.open', mock_open()) as mock_file:
        save_config(config_data, ".scaffolding_config.json")
        handle = mock_file()
        handle.write.assert_called()

def test_save_config_file_write_error():
    config_data = {"project_name": "test"}
    with patch('builtins.open', side_effect=Exception("Write error")):
        with pytest.raises(Exception):
            save_config(config_data, "test_config.json")

def test_load_default_config_delegates_to_get_project_config():
    with patch('src.scaffolding.config.get_project_config', return_value={"test": "data"}) as mock_get:
        result = load_default_config()
        assert result == {"test": "data"}
        mock_get.assert_called_once()

def test_save_default_config_delegates_to_save_config():
    config_data = {"project_name": "test"}
    with patch('src.scaffolding.config.save_config') as mock_save:
        save_default_config(config_data)
        mock_save.assert_called_once_with(config_data, ".scaffolding_config.json")

def test_get_project_config_empty_file(tmp_path):
    config_file = tmp_path / ".scaffolding_config.json"
    config_file.write_text("")
    
    with patch('pathlib.Path', return_value=Path(config_file)):
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data="")):
                result = get_project_config()
                assert result == {}

def test_get_project_config_no_file():
    with patch('pathlib.Path.exists', return_value=False):
        result = get_project_config()
        assert result == {}

def test_save_config_creates_file(tmp_path):
    config_data = {"project_name": "test-project", "version": "1.0"}
    config_file_path = tmp_path / "test_config.json"
    
    with patch('builtins.open', mock_open()) as mock_file:
        save_config(config_data, str(config_file_path))
        # Verify the file would be created with correct content
        with open(str(config_file_path), 'r') as f:
            saved_data = json.load(f)
            assert saved_data == config_data

def test_save_config_with_none_data():
    with patch('builtins.open', mock_open()) as mock_file:
        save_config(None)
        handle = mock_file()
        handle.write.assert_called()

def test_save_config_with_empty_dict():
    config_data = {}
    with patch('builtins.open', mock_open()) as mock_file:
        save_config(config_data)
        handle = mock_file()
        # Should write empty json object
        handle.write.assert_called()

def test_get_project_config_malformed_json():
    with patch('pathlib.Path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data='{"invalid": json}')):
            result = get_project_config()
            assert result == {}

def test_save_default_config_calls_save_config():
    config_data = {"key": "value"}
    with patch('src.scaffolding.config.save_config') as mock_save:
        save_default_config(config_data)
        mock_save.assert_called_once_with(config_data, ".scaffolding_config.json")

def test_load_default_config_returns_dict():
    with patch('src.scaffolding.config.get_project_config', return_value={"test": "value"}):
        result = load_default_config()
        assert result == {"test": "value"}

def test_save_config_with_special_characters():
    config_data = {"name": "test@project#1", "path": "/special/path/with/unicode/测试"}
    with patch('builtins.open', mock_open()) as mock_file:
        save_config(config_data, "special_config.json")
        handle = mock_file()
        handle.write.assert_called()

def test_get_project_config_with_nested_structure():
    complex_config = {
        "project": {
            "name": "test",
            "settings": {
                "debug": True,
                "version": "1.0"
            }
        }
    }
    
    with patch('pathlib.Path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data=json.dumps(complex_config))):
            result = get_project_config()
            assert result == complex_config

def test_save_config_overwrites_existing():
    config_data_1 = {"version": "1.0"}
    config_data_2 = {"version": "2.0"}
    
    with patch('builtins.open', mock_open()) as mock_file:
        save_config(config_data_1, "config.json")
        save_config(config_data_2, "config.json")
        # Should have been called twice
        assert mock_file().write.call_count == 2

def test_get_project_config_with_whitespace():
    with patch('pathlib.Path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data='  {"key": "value"}  ')):
            result = get_project_config()
            assert result == {"key": "value"}