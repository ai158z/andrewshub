import numpy as np
import math
from typing import List
import cmath

def quantum_fourier_transform(data: List[complex]) -> List[complex]:
    """
    Perform Quantum Fourier Transform on a list of complex numbers.
    
    Args:
        data: List of complex numbers representing quantum states
        
    Returns:
        Transformed data as list of complex numbers
    """
    # Validate input data
    if not isinstance(data, list):
        raise TypeError("Input data must be a list")
    
    if not data:
        return []
    
    # Check if all elements are numeric
    for i, x in enumerate(data):
        if not isinstance(x, (int, float, complex)):
            raise TypeError("All data elements must be numeric")
    
    # Convert data to numpy array for processing
    input_array = np.array(data)
    
    # Handle single element case
    if len(input_array) == 1:
        # For a single element, QFT is just the element itself
        return [complex(input_array[0])]
    
    # QFT implementation for multiple elements
    n = len(input_array)
    result = []
    
    # For each output element
    for k in range(n):
        sum_val = 0+0j
        # For each input element
        for j in range(n):
            # Calculate the QFT component: x_j * e^(-2πijk/N) / sqrt(N)
            angle = 2 * math.pi * j * k / n
            factor = cmath.exp(-1j * angle)
            sum_val += input_array[j] * factor
        result.append(sum_val / math.sqrt(n))
    
    return result