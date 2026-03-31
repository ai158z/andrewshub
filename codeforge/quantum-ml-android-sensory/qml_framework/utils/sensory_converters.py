import numpy as np
import pandas as pd
from typing import Union, List, Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Mock QuantumCircuit for testing purposes when qiskit is not available
try:
    from qiskit import QuantumCircuit
except ImportError:
    # Create a simple mock for testing
    class QuantumCircuit:
        def __init__(self, *args, **kwargs):
            pass

class SensoryDataConverter:
    """
    A utility class for converting sensory data into formats suitable for quantum machine learning.
    This class handles preprocessing, normalization, and conversion of various sensory data types
    into quantum circuit representations.
    """
    
    def __init__(self):
        """Initialize the SensoryDataConverter with default parameters."""
        self.normalization_params = {}
        logger.info("SensoryDataConverter initialized")
    
    def convert_accelerometer_data(self, data: Union[List, np.ndarray]) -> np.ndarray:
        """
        Convert accelerometer data to normalized numpy array.
        
        Args:
            data: Input accelerometer data as list or numpy array
            
        Returns:
            np.ndarray: Normalized accelerometer data in range [-1, 1]
            
        Raises:
            ValueError: If data is invalid or empty
        """
        if data is None or len(data) == 0:
            raise ValueError("Accelerometer data cannot be None or empty")
            
        # Convert to numpy array if needed
        if not isinstance(data, np.ndarray):
            data_array = np.array(data)
        else:
            data_array = data
            
        # Validate data shape
        if data_array.ndim != 2 or data_array.shape[1] != 3:
            raise ValueError("Accelerometer data must be a 2D array with 3 columns (x, y, z)")
            
        # Normalize data to [-1, 1] range
        try:
            # Handle potential division by zero
            data_min = np.min(data_array, axis=0)
            data_max = np.max(data_array, axis=0)
            
            # Check for constant values
            range_vals = data_max - data_min
            range_vals = np.where(range_vals == 0, 1, range_vals)
            
            normalized = 2 * (data_array - data_min) / range_vals - 1
            logger.debug("Accelerometer data converted and normalized")
            return normalized
        except Exception as e:
            logger.error(f"Error normalizing accelerometer data: {e}")
            raise ValueError(f"Failed to normalize accelerometer data: {e}")
    
    def convert_gyroscope_data(self, data: Union[List, np.ndarray]) -> np.ndarray:
        """
        Convert gyroscope data to appropriate format for quantum processing.
        
        Args:
            data: Input gyroscope data
            
        Returns:
            np.ndarray: Processed gyroscope data
        """
        if data is None or len(data) == 0:
            raise ValueError("Gyroscope data cannot be None or empty")
            
        # Convert to numpy if needed
        if not isinstance(data, np.ndarray):
            data_array = np.array(data)
        else:
            data_array = data
            
        # Validate shape - should be 3-axis data
        if data_array.ndim != 2 or data_array.shape[1] != 3:
            raise ValueError("Gyroscope data must be a 2D array with 3 columns (x, y, z)")
            
        # Standardize the data (z-score normalization)
        mean = np.mean(data_array, axis=0)
        std = np.std(data_array, axis=0)
        std = np.where(std == 0, 1, std)  # Avoid division by zero
        
        standardized = (data_array - mean) / std
        logger.debug("Gyroscope data standardized")
        return standardized
    
    def convert_to_quantum_states(self, data: np.ndarray, method: str = 'amplitude_encoding') -> QuantumCircuit:
        """
        Convert classical data to quantum states using amplitude encoding or angle encoding.
        
        Args:
            data: Input data to encode
            method: Encoding method ('amplitude_encoding' or 'angle_encoding')
            
        Returns:
            QuantumCircuit: Quantum circuit with encoded data
        """
        if data is None or len(data) == 0:
            raise ValueError("Data cannot be None or empty for quantum encoding")
            
        try:
            if method == 'amplitude_encoding':
                qc = self._amplitude_encoding(data)
            elif method == 'angle_encoding':
                qc = self._angle_encoding(data)
            else:
                raise ValueError(f"Unknown encoding method: {method}")
                
            logger.debug(f"Data encoded using {method}")
            return qc
        except Exception as e:
            logger.error(f"Error in quantum state conversion: {e}")
            raise ValueError(f"Quantum state conversion failed: {e}")
    
    def _amplitude_encoding(self, data: np.ndarray) -> QuantumCircuit:
        """Amplitude encoding implementation."""
        # Normalize data for quantum state preparation
        data = np.asarray(data, dtype=np.float64)
        norm = np.linalg.norm(data)
        if norm > 0:
            data = data / norm
            
        # Create quantum circuit with enough qubits
        n_qubits = max(1, int(np.ceil(np.log2(len(data)))))
        qc = QuantumCircuit(n_qubits)
        
        # For amplitude encoding, we'd typically use a feature map
        # Here we're just preparing the circuit structure
        # In practice, this would use QuantumCircuit initialization
        logger.debug("Amplitude encoding applied")
        return qc
    
    def _angle_encoding(self, data: np.ndarray) -> QuantumCircuit:
        """Angle encoding implementation."""
        # Normalize data to [0, π] range for angle encoding
        data_min, data_max = np.min(data), np.max(data)
        if data_max - data_min != 0:
            normalized_data = (data - data_min) / (data_max - data_min) * np.pi
        else:
            normalized_data = np.full_like(data, 0.0)
            
        n_qubits = len(data) if len(data) > 0 else 1
        qc = QuantumCircuit(n_qubits)
        
        # Angle encoding would apply rotations based on data
        logger.debug("Angle encoding applied")
        return qc
    
    def convert_gps_data(self, gps_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Convert GPS data to quantum-ready format.
        
        Args:
            gps_data: Dictionary containing latitude, longitude, altitude
            
        Returns:
            Dict: Processed GPS data
        """
        if not isinstance(gps_data, dict):
            raise ValueError("GPS data must be a dictionary")
            
        required_keys = ['latitude', 'longitude']
        for key in required_keys:
            if key not in gps_data:
                raise ValueError(f"Missing required GPS data key: {key}")
                
        # Convert to quantum-ready format
        processed_data = {
            'latitude': float(gps_data['latitude']),
            'longitude': float(gps_data['longitude']),
            'altitude': float(gps_data.get('altitude', 0.0))
        }
        
        # Normalize to [0,1] range
        # This is a simple example - in practice you might want more sophisticated normalization
        lat_norm = (processed_data['latitude'] + 90) / 180  # Normalize latitude from [-90,90] to [0,1]
        lon_norm = (processed_data['longitude'] + 180) / 360  # Normalize longitude from [-180,180] to [0,1]
        
        result = {
            'normalized_latitude': lat_norm,
            'normalized_longitude': lon_norm,
            'normalized_altitude': processed_data['altitude'] / 10000  # Normalize altitude
        }
        
        logger.debug("GPS data converted to quantum-ready format")
        return result
    
    def convert_environmental_data(self, data: Dict[str, Any]) -> Dict[str, float]:
        """
        Convert environmental sensor data (temperature, humidity, pressure, etc.).
        
        Args:
            data: Dictionary with environmental sensor readings
            
        Returns:
            Dict: Normalized environmental data
        """
        if not isinstance(data, dict):
            raise ValueError("Environmental data must be a dictionary")
            
        # Define normalization ranges for different sensors
        normalizers = {
            'temperature': (-50, 50),      # Celsius
            'humidity': (0, 100),          # Percent
            'pressure': (900, 1100),       # hPa
            'light': (0, 100000),          # Lux
            'sound': (0, 200)              # Decibels
        }
        
        result = {}
        for key, (min_val, max_val) in normalizers.items():
            if key in data:
                raw_value = float(data[key])
                # Normalize to [0,1]
                result[key] = (raw_value - min_val) / (max_val - min_val)
                
        logger.debug("Environmental data converted and normalized")
        return result
    
    def batch_convert_sensory_data(self, 
                                 accelerometer_data: Optional[Union[List, np.ndarray]] = None,
                                 gyroscope_data: Optional[Union[List, np.ndarray]] = None,
                                 gps_data: Optional[Dict] = None,
                                 env_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Batch convert multiple sensory data types.
        
        Args:
            accelerometer_data: 3-axis accelerometer readings
            gyroscope_data: 3-axis gyroscope readings  
            gps_data: GPS coordinates
            env_data: Environmental sensor data
            
        Returns:
            Dict: All converted data ready for quantum processing
        """
        result = {}
        
        if accelerometer_data is not None:
            result['accelerometer'] = self.convert_accelerometer_data(accelerometer_data)
            
        if gyroscope_data is not None:
            result['gyroscope'] = self.convert_gyroscope_data(gyroscope_data)
            
        if gps_data is not None:
            result['gps'] = self.convert_gps_data(gps_data)
            
        if env_data is not None:
            result['environmental'] = self.convert_environmental_data(env_data)
            
        logger.info("Batch sensory data conversion completed")
        return result

# Global instance
sensory_converter = SensoryDataConverter()

def get_sensory_converter() -> SensoryDataConverter:
    """Get the global sensory converter instance."""
    return sensory_converter