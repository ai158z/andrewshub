import json
import logging
from typing import Dict, Any, Union
import jsonschema as js

logger = logging.getLogger(__name__)

def validate_json_schema(data: Dict, schema: Dict) -> bool:
    """
    Validate JSON data against a given schema using jsonschema library.
    
    Args:
        data: JSON data as a dictionary
        schema: JSON schema as a dictionary
        
    Returns:
        bool: True if data is valid according to schema, False otherwise
    """
    try:
        js.validate(instance=data, schema=schema)
        return True
    except js.ValidationError as e:
        logger.warning(f"JSON schema validation error: {e.message}")
        return False
    except js.SchemaError as e:
        logger.error(f"Invalid schema: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during schema validation: {e}")
        return False

import json
import logging
from typing import Dict, Any
import jsonschema as js

logger = logging.getLogger(__name__)

def validate_json_schema(data: Dict, schema: Dict) -> bool:
    """
    Validate JSON data against a given schema using jsonschema library.
    
    Args:
        data: JSON data as a dictionary
        schema: JSON schema as a dictionary
        
    Returns:
        bool: True if data is valid according to schema, False otherwise
    """
    try:
        js.validate(instance=data, schema=schema)
        return True
    except js.ValidationError as e:
        logger.warning(f"JSON schema validation error: {e.message}")
        return False
    except js.SchemaError as e:
        logger.error(f"Invalid schema: {e}")
        return False
    except Exception as e:
        logger.error(f"Error during schema validation: {e}")
        return False

import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def is_valid_json_file(filepath: str) -> bool:
    """
    Check if a file contains valid JSON.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        bool: True if file contains valid JSON, False otherwise
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except json.JSONDecodeError as e:
        logger.warning(f"JSON decode error in {filepath}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error reading file {filepath}: {e}")
        return False

import json
import logging
from typing import Dict, Any

def is_valid_json_file(filepath: str) -> bool:
    """
    Check if a file contains valid JSON.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        bool: True if file contains valid JSON, False otherwise
    """
    try:
        with open(filepath, 'r') as f:
            json.load(f)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return False