import numpy as np
import logging
from typing import Dict, Any, List
from src.utils.quantum_math import quantum_fourier_transform
from src.utils.signal_processing import process_signal

logger = logging.getLogger(__name__)

class QuantumProcessor:
    def __init__(self):
        self.quantum_enabled = True
        self.processed_states = []

    def process_quantum_state(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Validate input data
            if not isinstance(input_data, dict):
                raise ValueError("Input data must be a dictionary")
            
            # Process the quantum state
            processed_signal = self._apply_quantum_transformations(input_data)
            
            # Apply quantum processing
            quantum_state = {
                "status": "processed",
                "data": processed_signal,
                "metadata": {
                    "timestamp": input_data.get("timestamp", None),
                    "processor": "quantum_state_processor"
                }
            }
            
            return quantum_state
        except Exception as e:
            logger.error(f"Quantum state processing failed: {str(e)}")
            raise RuntimeError(f"Quantum processing error: {str(e)}")

    def _apply_quantum_transformations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Extract signal data
        signal_data = data.get('data', [])
        
        # Handle case where data key is missing or empty
        if signal_data is None or (isinstance(signal_data, list) and len(signal_data) == 0):
            # If no data provided, return a processed state of False
            return {
                "processed": False,
                "result": None
            }
        
        # Apply signal processing
        processed_signal = process_signal(signal_data)
        
        # Apply quantum fourier transform
        qft_result = quantum_fourier_transform(processed_signal)
        
        # Return processed state
        return {
            "processed": True,
            "signal": processed_signal,
            "qft_result": qft_result,
            "amplitude": np.abs(qft_result),
            "phase": np.angle(qft_result)
        }