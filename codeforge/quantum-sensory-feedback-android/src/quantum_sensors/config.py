import os
from typing import Dict, Any, Optional, Union
from pathlib import Path
import json
import logging

logger = logging.get_logger(__name__)

class ConfigManager:
    """Configuration manager for quantum sensor system."""
    
    def __init__(self, config_file=None):
        self._config: Dict[str, Any] = {}
        self._config_file: Optional[Path] = None
        self._load_default_config()
    
    def _load_default_config(self) -> None:
        """Load default configuration values."""
        self._config = {
            "sensor_refresh_rate": 60,
            "fusion_algorithm": "quantum_state_preserving",
            "zeno_stabilization": True,
            "codonic_processing": True,

    def get_config(self, key: str = None) -> Any:
        """
        Get configuration value(s).
        
        Args:
            key: Configuration key to retrieve. If None, returns all config.
        """
        if key is None:
            return self._config.copy()
        
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        
        if key not in self._config:
            raise KeyError(f"Configuration key '{key}' not found")
        
        return self._config[key]

    def set_config(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key to set
            value: Value to set for the key
        """
        if key not in self._config:
            raise KeyError(f"Configuration key '{key}' not found")
        
        self._config[key] = value
        return self._config[key]

    def load_from_file(self, config_file: str) -> None:
        """Load configuration from a JSON file.
        
        Args:
            config_file: Path to the configuration file
        """
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                self._config.update(file_config)
            logger.info(f"Configuration loaded from {config_file}")
        except Exception as e:
            logger.error(f"Failed to load configuration from file: {e}")
            raise

    def save_to_file(self, filename: str) -> None:
        """Save configuration to a file.
        
        Args:
            filename: Path to save configuration to
        """
        # This would be the implementation for saving config
        try:
            with open(filename, 'w') as f:
                json.dump(self._config, f)
            logger.info(f"Configuration saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save configuration to file: {e}")
            raise

    def save_to_file(self, config_file: str) -> None:
        """Save configuration to a file."""
        try:
            with open(config_file, 'w') as f:
                json.dump(self._config, f)