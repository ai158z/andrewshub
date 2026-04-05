import hashlib
import os
from typing import Union

def sha3_512_hash(data: bytes) -> bytes:
    """
    Generate a SHA3-512 hash of the provided data.
    
    Args:
        data: Input data as bytes to be hashed
        
    Returns:
        bytes: The SHA3-512 hash of the input data
    """
    if not isinstance(data, bytes):
        raise TypeError("Data must be of type bytes")
    
    if not data:
        raise ValueError("No data provided")
    
    if len(data) == 0:
        raise ValueError("Data cannot be empty")
    
    # Create a sha3_512_hash object
    hash_obj = hashlib.sha3_512()
    hash_obj.update(data)
    return hash_obj.digest()

def sha3_512_hash_hex(data: bytes) -> str:
    """
    Generate a hex string of the SHA3-512 hash.
    
    Args:
        data: Input data as bytes to be hashed
        
    Returns:
        str: Hexadecimal string representation of the hash
    """
    return sha3_512_hash(data).hex()

def get_file_hash(file_path: str) -> str:
    """
    Get the SHA3-512 hash of a file's contents.
    
    Args:
        file_path: Path to file to be hashed
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'rb') as f:
        file_content = f.read()
    
    return sha3_512_hash(file_content).hex()

def validate_environment_variables(*args):
    """
    Validate that required environment variables are set.
    """
    env_vars = {}
    for var in args:
        if var not in os.environ:
            raise EnvironmentError(f"Environment variable {var} not found")
        env_vars[var] = os.environ[var]
    return env_vars

def format_hash_for_display(hash_bytes: bytes, chunk_size: int = 4) -> str:
    """
    Format a hash string for display.
    """
    if not hash_bytes:
        return ""
    
    hex_string = hash_bytes.hex()
    # Format the hash string for better display
    formatted = ""
    for i in range(0, len(hex_string), chunk_size*2):
        if i > 0:
            formatted += " "
        formatted += hex_string[i: i + chunk_size*2]
    return formatted

def validate_data_integrity(data: bytes, hash_string: str, algorithm: str = "sha3_512") -> bool:
    """
    Validate that a data matches a specific hash.
    """
    if not isinstance(data, bytes):
        raise TypeError("Data must be of type bytes")
    
    if algorithm == "sha3_512":
        return sha3_512_hash(data).hex() == hash_string
    else:
        raise ValueError("Unsupported algorithm")