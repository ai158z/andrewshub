import hashlib
from typing import Union

def sha3_512_hash(data: Union[bytes, str]) -> bytes:
    """
    Generate a SHA3-512 hash of the provided data.
    
    Args:
        data: The data to hash, either as bytes or string
        
    Returns:
        bytes: The SHA3-512 hash digest
        
    Raises:
        TypeError: If data is not bytes or string
        ValueError: If data is empty
    """
    # Handle None input specifically
    if data is None:
        raise ValueError("Data cannot be empty")
    
    # Check for empty data
    if not data:
        raise ValueError("Data cannot be empty")
    
    # Convert string to bytes if necessary
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        raise TypeError("Data must be bytes or string")
    
    # Generate the hash
    hasher = hashlib.sha3_512()
    hasher.update(data)
    return hasher.digest()