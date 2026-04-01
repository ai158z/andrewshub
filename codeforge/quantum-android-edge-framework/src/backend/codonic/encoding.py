import logging
from typing import Dict, Any, Union
import numpy as np
from src.backend.quantum.encryption import encrypt, decrypt

logger = logging.getLogger(__name__)

class CodonicEncoder:
    def __init__(self):
        self.sensory_symbols = {
            'position': 'POS',
            'velocity': 'VEL',
            'orientation': 'ORI',
            'temperature': 'TEMP',
            'pressure': 'PRES',
            'humidity': 'HUM'
        }
        
        self.motor_symbols = {
            'rotation': 'ROT',
            'translation': 'TRANS',
            'actuation': 'ACT'
        }

    def encode_sensory_input(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encode raw sensor data into symbolic representation
        
        Args:
            sensor_data: Dictionary containing raw sensor data
            
        Returns:
            Dict containing encoded symbolic data
        """
        if not isinstance(sensor_data, dict):
            raise ValueError("sensor_data must be a dictionary")
            
        encoded_output = {
            'timestamp': sensor_data.get('timestamp', None),
            'node_id': sensor_data.get('node_id', None),
            'encoded_data': {}
        }
        
        # Map raw sensor values to symbolic representations
        for sensor_type, value in sensor_data.items():
            if sensor_type in self.sensory_symbols:
                symbol = self.sensory_symbols[sensor_type]
                # Normalize and encode the value
                if isinstance(value, (int, float, str)):
                    # Convert to symbolic representation using quantization
                    normalized_value = self._normalize_value(value)
                    encoded_output['encoded_data'][symbol] = normalized_value
                elif isinstance(value, dict):
                    encoded_output['encoded_data'][symbol] = {
                        k: self._normalize_value(v) for k, v in value.items()
                    }
                else:
                    encoded_output['encoded_data'][symbol] = value
                    
        logger.debug(f"Encoded sensory input: {encoded_output}")
        return encoded_output

    def decode_motor_output(self, encoded_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decode symbolic motor commands to executable actions
        
        Args:
            encoded_data: Dictionary containing encoded symbolic data
            
        Returns:
            Dict containing decoded motor commands
        """
        if not isinstance(encoded_data, dict):
            raise ValueError("encoded_data must be a dictionary")
            
        if 'encoded_data' not in encoded_data:
            raise ValueError("encoded_data must contain 'encoded_data' key")
            
        decoded_output = {
            'timestamp': encoded_data.get('timestamp'),
            'node_id': encoded_data.get('node_id'),
            'decoded_data': {}
        }
        
        # Decode symbolic motor commands
        for symbol, value in encoded_data['encoded_data'].items():
            if symbol in self.sensory_symbols.values():
                # Find the original key for the symbol
                original_key = next((k for k, v in self.sensory_symbols.items() if v == symbol), symbol)
                decoded_output['decoded_data'][original_key] = value
            elif symbol in self.motor_symbols.values():
                original_key = next((k for k, v in self.motor_symbols.items() if v == symbol), symbol)
                decoded_output['decoded_data'][original_key] = value
            else:
                decoded_output['decoded_data'][symbol] = value
        return decoded_output

    def _normalize_value(self, value: Union[int, float, str]) -> float:
        """
        Normalize sensor values to standard range
        
        Args:
            value: Raw sensor value
            
        Returns:
            Normalized value
        """
        if isinstance(value, (int, float)):
            # Apply some normalization (example: scaling to 0-1 range)
            return float(1 / (1 + np.exp(-float(value)/100)))  # Sigmoid-like normalization
        elif isinstance(value, str):
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0
        return float(value)

# Module-level instances for backward compatibility
_encoder = None

def encode_sensory_input(sensor_data: dict) -> dict:
    """
    Encode raw sensor data into symbolic representation
    
    Args:
        sensor_data: Dictionary containing raw sensor data
        
    Returns:
        Dict containing raw sensor data
    """
    global _encoder
    if _encoder is None:
        _encoder = CodonicEncoder()
    return _encoder.encode_sensory_input(sensor_data)

def decode_motor_output(encoded_data: dict) -> dict:
    """
    Decode symbolic motor commands to executable actions
    
    Args:
        encoded_data: Dictionary containing encoded symbolic data
        
    Returns:
        Dict containing decoded motor commands
    """
    global _encoder
    if _encoder is None:
        _encoder = CodonicEncoder()
    return _encoder.decode_motor_output(encoded_data)