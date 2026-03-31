import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Union
from qiskit import QuantumCircuit
from qiskit_machine_learning.algorithms import VQC
from qiskit_machine_learning.kernels import QuantumKernel
import logging

logger = logging.getLogger(__name__)

class SensoryInputProcessor:
    """Processor for handling sensory input data from Android devices"""
    
    def __init__(self):
        self.data_buffer: List[Dict[str, Any]] = []
        self.processed_data: List[Dict[str, Any]] = []
        self.quantum_model: Optional[VQC] = None
        self.kernel: Optional[QuantumKernel] = None
        
    def process_sensory_data(self, data: Union[List[Dict], Dict]) -> Dict[str, Any]:
        """
        Process sensory data from various sources
        
        Args:
            data: Input sensory data as list of dictionaries or single dictionary
            
        Returns:
            Dict containing processed data and metadata
        """
        try:
            # Handle both single dict and list of dicts input
            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                raise ValueError("Data must be a dictionary or list of dictionaries")
                
            # Process each data point
            processed_points = []
            for data_point in data:
                if not isinstance(data_point, dict):
                    raise ValueError("Each data point must be a dictionary")
                processed_points.append(self._process_single_data_point(data_point))
                
            # Return combined results
            return {
                "processed_data": processed_points,
                "raw_data": data,
                "timestamp": pd.Timestamp.now().isoformat(),
                "status": "processed"
            }
            
        except Exception as e:
            logger.error(f"Error processing sensory data: {str(e)}")
            raise
            
    def _process_single_data_point(self, data_point: Dict) -> Dict[str, Any]:
        """Process a single data point"""
        try:
            # Validate required fields
            required_fields = ['timestamp', 'sensor_type', 'values']
            for field in required_fields:
                if field not in data_point:
                    raise ValueError(f"Missing required field: {field}")
                    
            # Convert values to numpy array for processing
            values = np.array(data_point['values'])
            
            # Apply quantum feature mapping if available
            if self.kernel is not None:
                # Quantum feature map would be applied here
                pass
                
            return {
                "sensor_type": data_point.get('sensor_type'),
                "timestamp": data_point.get('timestamp'),
                "values": values.tolist(),
                "processed": True
            }
            
        except Exception as e:
            logger.error(f"Error processing data point: {str(e)}")
            raise

    def _validate_sensory_data(self, data: Dict) -> bool:
        """Validate sensory data format and content"""
        required_fields = ['timestamp', 'sensor_type', 'values']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        return True

# Global instance
sensory_processor = SensoryInputProcessor()

# Convenience function for external use
def process_sensory_data(data: Union[List[Dict], Dict]) -> Dict[str, Any]:
    """
    Main function to process sensory data
    
    Args:
        data: Input sensory data
        
    Returns:
        Processed data result
    """
    return sensory_processor.process_sensory_data(data)