import json
import logging
from typing import Dict, Any, Union
from collections import deque

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def flatten_dict(d: Dict[str, Any], separator: str = '_') -> Dict[str, Any]:
    """
    Flatten a nested dictionary structure using the specified separator.
    
    Args:
        d: Dictionary to flatten
        separator: String separator for nested keys (default: '_')
        
    Returns:
        Flattened dictionary with dot-separated keys for nested elements
    """
    if not isinstance(d, dict):
        raise TypeError("Input must be a dictionary")
    
    flattened = {}
    queue = deque([([], d)])  # Queue of (key_path, value) tuples
    
    while queue:
        key_path, value = queue.popleft()
        
        if isinstance(value, dict):
            # Add all dict items to queue with updated key paths
            for k, v in value.items():
                new_key_path = key_path + [k]
                queue.append((new_key_path, v))
        elif isinstance(value, list):
            # For lists, we create indexed keys
            for i, item in enumerate(value):
                new_key_path = key_path + [str(i)]
                queue.append((new_key_path, item))
        else:
            # For primitive values, add to flattened dict
            if key_path:  # Only create key if key_path is not empty
                key = separator.join(key_path)
                flattened[key] = value
    
    return flattened

def read_json_file(filepath: str) -> Dict[str, Any]:
    """
    Read and parse a JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Parsed JSON data as dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Successfully read JSON file: {filepath}")
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {filepath}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error reading file {filepath}: {str(e)}")
        raise