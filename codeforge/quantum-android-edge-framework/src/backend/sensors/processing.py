import numpy as np
from typing import Dict, Any, Union
from scipy import signal
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class SensorData(BaseModel):
    timestamp: float
    data: Dict[str, Any]
    node_id: str


class FilteredData(BaseModel):
    timestamp: float
    filtered_values: Dict[str, float]
    sensor_id: str


def process_sensor_data(raw_data: bytes) -> SensorData:
    """
    Process raw sensor data bytes into structured SensorData object.
    
    Args:
        raw_data: Raw bytes from sensor input
        
    Returns:
        SensorData: Processed sensor data model
    """
    try:
        # Handle None input
        if raw_data is None:
            raise ValueError("Input data cannot be None")
        
        # Handle non-bytes input
        if not isinstance(raw_data, bytes):
            raise TypeError("Input data must be bytes")
            
        # Handle empty bytes
        if len(raw_data) == 0:
            raise ValueError("Empty bytes provided")
        
        # Parse raw bytes into structured data
        import json
        parsed_data = json.loads(raw_data.decode('utf-8')) if raw_data else {}
        
        return SensorData(
            timestamp=parsed_data.get('timestamp', 0.0),
            data=parsed_data.get('data', {}),
            node_id=parsed_data.get('node_id', 'unknown')
        )
    except Exception as e:
        logger.error(f"Error processing sensor data: {str(e)}")
        raise ValueError(f"Failed to process sensor data: {str(e)}")


def filter_noise(sensor_input: SensorData) -> FilteredData:
    """
    Apply digital filtering to sensor input data to reduce noise.
    
    Args:
        sensor_input: Raw sensor data to filter
        
    Returns:
        FilteredData: Noise-filtered sensor data
    """
    try:
        # Extract sensor values
        values = list(sensor_input.data.values())
        if not values:
            return FilteredData(
                timestamp=sensor_input.timestamp,
                filtered_values={},
                sensor_id=sensor_input.node_id
            )
        
        # Convert to numpy array for processing
        data_array = np.array(values, dtype=float)
        
        # Apply low-pass filter to remove high frequency noise
        if len(data_array) > 1:
            # Design a Butterworth filter
            # Filter order: 3, Cutoff frequency: 0.2 (normalized), Sampling frequency: 1.0
            sos = signal.butter(3, 0.2, 'low', output='sos')
            # Apply filter to data
            filtered_data = signal.sosfilt(sos, data_array)
        else:
            # If only one data point, return as is
            filtered_data = data_array
            
        # Create filtered result mapping
        filtered_values = {}
        original_keys = list(sensor_input.data.keys())
        for i, val in enumerate(filtered_data):
            if i < len(original_keys):
                filtered_values[original_keys[i]] = val
        
        return FilteredData(
            timestamp=sensor_input.timestamp,
            filtered_values=filtered_values,
            sensor_id=sensor_input.node_id
        )
    except Exception as e:
        logger.error(f"Error applying filter: {str(e)}")
        raise ValueError(f"Filtering failed: {str(e)}")