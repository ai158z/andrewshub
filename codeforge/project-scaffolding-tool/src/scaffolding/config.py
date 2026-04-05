import json
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def get_project_config():
    """Load project configuration from a config file"""
    config_path = Path(".scaffolding_config.json")
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading config: {e}")
            return {}
    return {}

def save_config(config_data: dict, config_file_path: str = ".scaffolding_config.json"):
    """Save project configuration to a config file"""
    try:
        with open(config_file_path, 'w') as f:
            json.dump(config_data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving config: {e}")
    return

def load_default_config():
    """Load the default configuration to a file"""
    return get_project_config()

def save_default_config(config_data: dict) -> None:
    config_path = ".scaffolding_config.json"
    save_config(config_data, config_path)
    return