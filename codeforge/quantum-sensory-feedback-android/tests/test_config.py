import json
import logging
import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.quantum_sensors.config import ConfigManager

class TestConfigManager:
    """Test suite for ConfigManager class."""
    
    def test_init_loads_default_config(self):
        """Test that initialization loads default configuration."""
        config_manager = ConfigManager()
        config = config_manager.get_config()
        
        # Check that default values are loaded
        assert config["sensor_refresh_rate"] == 60
        assert config["fusion_algorithm"] == "quantum_state_preserving"
        assert config["zeno_stabilization"] is True
        assert config["codonic_processing"] is True
        assert config["entanglement_enabled"] is True
        assert config["ros2_node_name"] == "quantum_sensors_node"
        assert config["log_level"] == "INFO"
    
    def test_get_config_all(self):
        """Test getting all configuration."""
        config_manager = ConfigManager()
        config = config_manager.get_config()
        assert isinstance(config, dict)
        assert len(config) > 0
    
    def test_get_config_specific_key(self):
        """Test getting specific configuration value."""
        config_manager = ConfigManager()
        value = config_manager.get_config("sensor_refresh_rate")
        assert value == 60
    
    def test_get_config_nonexistent_key(self):
        """Test getting non-existent configuration key raises KeyError."""
        config_manager = ConfigManager()
        with pytest.raises(KeyError, match="Configuration key 'nonexistent_key' not found"):
            config_manager.get_config("nonexistent_key")
    
    def test_get_config_invalid_key_type(self):
        """Test getting config with invalid key type raises TypeError."""
        config_manager = ConfigManager()
        with pytest.raises(TypeError, match="Key must be a string"):
            config_manager.get_config(123)
    
    def test_set_config_updates_existing(self, caplog):
        """Test updating existing configuration value."""
        config_manager = ConfigManager()
        with caplog.at_level(logging.INFO):
            config_manager.set_config("sensor_refresh_rate", 120)
            assert "Updating config: sensor_refresh_rate = 120" in caplog.text
        
        value = config_manager.get_config("sensor_refresh_rate")
        assert value == 120
    
    def test_set_config_adds_new(self, caplog):
        """Test adding new configuration value."""
        config_manager = ConfigManager()
        with caplog.at_level(logging.INFO):
            config_manager.set_config("new_setting", "test_value")
            assert "Setting new config: new_setting = test_value" in caplog.text
        
        value = config_manager.get_config("new_setting")
        assert value == "test_value"
    
    def test_set_config_invalid_key_type(self):
        """Test setting config with invalid key type raises TypeError."""
        config_manager = ConfigManager()
        with pytest.raises(TypeError, match="Key must be a string"):
            config_manager.set_config(123, "value")
    
    def test_load_from_file_success(self, tmp_path, caplog):
        """Test loading configuration from file."""
        # Create a temporary config file
        config_file = tmp_path / "config.json"
        config_data = {
            "sensor_refresh_rate": 30,
            "custom_setting": "custom_value"
        }
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        config_manager = ConfigManager()
        with caplog.at_level(logging.INFO):
            config_manager.load_from_file(str(config_file))
            assert f"Configuration loaded from {config_file}" in caplog.text
        
        # Verify the configuration was loaded
        assert config_manager.get_config("sensor_refresh_rate") == 30
        assert config_manager.get_config("custom_setting") == "custom_value"
    
    def test_load_from_file_not_found(self):
        """Test loading configuration from non-existent file."""
        config_manager = ConfigManager()
        with pytest.raises(Exception):
            config_manager.load_from_file("nonexistent_file.json")
    
    def test_load_from_file_invalid_json(self):
        """Test loading configuration from invalid JSON file."""
        config_manager = ConfigManager()
        with patch("builtins.open", mock_open(read_data="invalid json content")):
            with pytest.raises(json.JSONDecodeError):
                config_manager.load_from_file("invalid.json")
    
    def test_save_to_file_success(self, tmp_path, caplog):
        """Test saving configuration to file."""
        config_manager = ConfigManager()
        config_file = tmp_path / "saved_config.json"
        
        with caplog.at_level(logging.INFO):
            config_manager.save_to_file(str(config_file))
            assert f"Configuration saved to {config_file}" in caplog.text
        
        # Verify file was created with correct content
        assert config_file.exists()
        with open(config_file, 'r') as f:
            saved_data = json.load(f)
            assert isinstance(saved_data, dict)
    
    def test_save_to_file_error(self, tmp_path):
        """Test saving configuration to invalid path."""
        config_manager = ConfigManager()
        invalid_path = tmp_path / "nonexistent" / "config.json"
        with pytest.raises(Exception):
            config_manager.save_to_file(str(invalid_path))
    
    def test_config_key_type_validation(self):
        """Test type validation for config keys."""
        config_manager = ConfigManager()
        with pytest.raises(TypeError):
            config_manager.set_config(123, "value")
        with pytest.raises(TypeError):
            config_manager.get_config(123)
    
    def test_config_default_values(self):
        """Test that all default configuration values are properly set."""
        config_manager = ConfigManager()
        defaults = config_manager.get_config()
        
        expected_defaults = {
            "sensor_refresh_rate": 60,
            "fusion_algorithm": "quantum_state_preserving",
            "zeno_stabilization": True,
            "codonic_processing": True,
            "entanglement_enabled": True,
            "ros2_node_name": "quantum_sensors_node",
            "log_level": "INFO"
        }
        
        for key, expected_value in expected_defaults.items():
            assert defaults[key] == expected_value, f"Default value mismatch for {key}"