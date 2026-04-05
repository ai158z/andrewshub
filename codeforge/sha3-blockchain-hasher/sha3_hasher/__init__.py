import os
import logging
from typing import Optional

# Version information
__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# Environment variables 
DATABASE_URL: Optional[str] = os.environ.get("DATABASE_URL")
REDIS_URL: Optional[str] = os.environ.get("REDIS_URL")

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configure console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def get_version() -> str:
    """
    Get the current version of the sha3-blockchain-hasher library.
    
    Returns:
        str: The version string in semantic versioning format.
    """
    return __version__

# Import core functionality
try:
    from .core import sha3_512_hash
except ImportError:
    sha3_512_hash = None

try:
    from .benchmark import benchmark_hashing_speed
except ImportError:
    benchmark_hashing_speed = None

try:
    from .ros2_node import create_ros2_node
except ImportError:
    create_ros2_node = None

try:
    from .utils import sha3_512_hash as util_sha3_512_hash
except ImportError:
    util_sha3_512_hash = None

# Update __all__ based on what was successfully imported
__all__ = [
    'get_version',
]

# Only include functions that were successfully imported
if sha3_512_hash is not None:
    __all__.append('sha3_512_hash')

if benchmark_hashing_speed is not None:
    __all__.append('benchmark_hashing_speed')

if create_ros2_node is not None:
    __all__.append('create_ros2_node')

if util_sha3_512_hash is not None:
    __all__.append('util_sha3_512_hash')