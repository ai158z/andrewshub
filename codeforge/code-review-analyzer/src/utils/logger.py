import logging
import sys
from typing import Optional

# Module level logger instance
_logger: Optional[logging.Logger] = None

def get_logger():
    """Get the module level logger instance."""
    return _logger

def setup_logger(level: str = "INFO") -> logging.Logger:
    """
    Set up and configure a logger with the specified verbosity level.
    
    Args:
        level: Logging level as string (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR')
        
    Returns:
        Configured logger instance
    """
    global _logger
    
    # Return existing logger if already set up
    if _logger is not None:
        _logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        return _logger
    
    # Create logger
    logger = logging.getLogger("code_review_analyzer")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Create console handler and set level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - code_review_analyzer - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    # Store the logger for reuse
    _logger = logger
    
    return logger

def log(message: str, level: str = "INFO") -> None:
    """
    Log a message with the specified level.
    
    Args:
        message: Message to log
        level: Logging level as string (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR')
    """
    logger = setup_logger()
    level_upper = level.upper()
    log_level = getattr(logging, level_upper, logging.INFO)
    log_func_name = level.lower()
    
    # Handle invalid level names
    if level_upper not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        log_func_name = 'info'
    
    if hasattr(logger, log_func_name):
        log_func = getattr(logger, log_func_name)
    else:
        log_func = logger.info
    log_func(message)

# Ensure the functions are available at module level
__all__ = ['get_logger', 'setup_logger', 'log']