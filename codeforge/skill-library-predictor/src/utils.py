import logging
from typing import Dict, List, Union
import numpy as np
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)

def calculate_success_rate(success_count: int, total_count: int) -> float:
    """
    Calculate the success rate as a percentage.
    
    Args:
        success_count: Number of successful outcomes
        total_count: Total number of outcomes
        
    Returns:
        Success rate as a percentage value
    """
    if total_count == 0:
        return 0.0
    return (success_count / total_count) * 100

def normalize_data(data: Union[List, np.ndarray], feature_range: tuple = (0, 1)) -> np.ndarray:
    """
    Normalize data to a specified feature range using Min-Max scaling.
    
    Args:
        data: Input data array
        feature_range: Tuple defining the feature range for normalization
        
    Returns:
        Normalized data array
    """
    if len(data) == 0:
        return np.array([])

    scaler = MinMaxScaler(feature_range=feature_range)
    
    # Reshape data if it's 1D
    if isinstance(data, list) or (isinstance(data, np.ndarray) and data.ndim == 1):
        data_array = np.array(data).reshape(-1, 1)
    else:
        data_array = np.array(data)
        
    normalized = scaler.fit_transform(data_array)
    return normalized.flatten() if normalized.shape[1] == 1 else normalized

def format_response(data: Dict) -> Dict:
    """
    Format the response data according to the required schema.
    
    Args:
        data: Data to be formatted
        
    Returns:
        Formatted response dictionary
    """
    return {
        "status": "success",
        "data": data,
        "message": "Response formatted successfully"
    }