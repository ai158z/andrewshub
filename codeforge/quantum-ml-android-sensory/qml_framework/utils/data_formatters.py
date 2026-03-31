import numpy as np
import pandas as pd
from typing import Union, List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def format_sensory_data(data: Union[List, Dict, pd.DataFrame]) -> Dict[str, Any]:
    """Format sensory data into a standard dictionary structure.
    
    Args:
        data: Input data as list, dict, or DataFrame
        
    Returns:
        Dict with 'features' and 'metadata' keys
    """
    result = {
        'features': {},
        'metadata': {}
    }
    
    try:
        if isinstance(data, dict):
            result['features'] = data.copy()
        elif isinstance(data, list):
            result['features'] = {f'feature_{i}': val for i, val in enumerate(data)}
        elif isinstance(data, pd.DataFrame):
            result['features'] = {col: data[col].tolist() for col in data.columns}
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")
            
        # Add metadata
        result['metadata'] = {
            'data_type': type(data).__name__,
            'shape': getattr(data, 'shape', (len(data),) if isinstance(data, (list, dict)) else None)
        }
    except Exception as e:
        logger.error(f"Error formatting data: {str(e)}")
        raise
    
    return result

def normalize_quantum_data(data: Union[List, Dict], precision: int = 6) -> Union[Dict, List]:
    """Normalize quantum data values to standard format.
    
    Args:
        data: Input data
        precision: Number of decimal places to round to
        
    Returns:
        Dict with normalized values or the original data if it's a list
    """
    if isinstance(data, dict):
        normalized = {}
        for key, value in data.items():
            if isinstance(value, float):
                normalized[key] = round(value, precision)
            elif isinstance(value, list) and all(isinstance(x, (int, float)) for x in value):
                normalized[key] = [round(x, precision) for x in value]
            else:
                normalized[key] = value
        return normalized
    elif isinstance(data, list):
        # If it's a list, return as is
        return data
    return data

def validate_data_structure(data: Dict) -> bool:
    """Validate that data has expected structure.
    
    Args:
        data: Data dictionary to validate
        
    Returns:
        True if valid structure
    """
    required_keys = ['features', 'metadata']
    return isinstance(data, dict) and all(key in data for key in required_keys)

def convert_to_dataframe(data: Dict) -> pd.DataFrame:
    """Convert formatted data to pandas DataFrame.
    
    Args:
        data: Formatted data dictionary
        
    Returns:
        DataFrame representation of data
    """
    if validate_data_structure(data):
        features = data.get('features', {})
        if isinstance(features, dict):
            return pd.DataFrame([features]) if features else pd.DataFrame()
        elif isinstance(features, list) and all(isinstance(item, dict) for item in features):
            return pd.DataFrame(features)
        else:
            return pd.DataFrame()
    return pd.DataFrame()