"""
Formats package initialization module.
"""

try:
    from .ethereum import EthereumFormat
except ImportError:
    EthereumFormat = None

try:
    from .bitcoin import BitcoinFormat
except ImportError:
    BitcoinFormat = None

try:
    from .generic import GenericFormat
except ImportError:
    GenericFormat = None

# Build __all__ dynamically based on what was successfully imported
__all__ = []
if EthereumFormat is not None:
    __all__.append('EthereumFormat')
if BitcoinFormat is not None:
    __all__.append('BitcoinFormat')
if GenericFormat is not None:
    __all__.append('GenericFormat')

__all__.append('get_format_classes')

def get_format_classes():
    """Return available format classes"""
    classes = []
    if EthereumFormat is not None:
        classes.append(EthereumFormat)
    if BitcoinFormat is not None:
        classes.append(BitcoinFormat)
    if GenericFormat is not None:
        classes.append(GenericFormat)
    return classes