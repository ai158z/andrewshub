import numpy as np
from typing import List, Union
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_signal(signal: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    Process a sensory signal by applying noise reduction, normalization, and feature extraction.
    
    Args:
        signal: A list of numerical values representing the sensory signal
        
    Returns:
        A list of processed signal values
    """
    try:
        # Validate input
        if signal is None:
            raise TypeError("Signal cannot be None")
        
        if not signal:  # Empty list
            raise ValueError("Signal cannot be empty")
        
        # Convert to numpy array for processing
        signal_array = np.array(signal, dtype=float)
        
        # Check for non-numerical values
        if not all(isinstance(x, (int, float)) and np.isfinite(x) for x in signal_array):
            raise TypeError("All signal values must be numerical")
        
        # Apply noise reduction using a simple moving average filter
        window_size = min(5, len(signal_array))
        if window_size % 2 == 0:
            window_size = max(1, window_size - 1)  # Ensure odd window size
        
        if window_size > 1:
            padded_signal = np.pad(signal_array, (window_size//2, window_size//2), mode='edge')
            filtered_signal = np.convolve(padded_signal, np.ones(window_size)/window_size, mode='valid')
        else:
            filtered_signal = signal_array
            
        # Normalize the signal to 0-1 range
        signal_min = filtered_signal.min()
        signal_max = filtered_signal.max()
        if signal_max != signal_min:
            normalized_signal = (filtered_signal - signal_min) / (signal_max - signal_min)
        else:
            # When all values are the same, they should all normalize to 0
            normalized_signal = np.zeros_like(filtered_signal)
            
        # Convert back to list and return
        result = normalized_signal.tolist()
        logger.info("Signal processed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error processing signal: {str(e)}")
        raise