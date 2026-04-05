import importlib
import logging
from typing import Any, Dict, Union

logger = logging.getLogger(__name__)

def validate_observation_space(space: Union[Any, Dict]) -> bool:
    """
    Validate that the observation space is of a supported type.
    
    Args:
        space: The observation space to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        import gym
        from gym import spaces
    except ImportError:
        logger.warning("gym not available, skipping space validation")
        return True  # Assume valid if we can't check
    
    if isinstance(space, dict):
        space = space.get('observation_space', None)
        if space is None:
            return False

    if space is None:
        return False
    
    if not isinstance(space, spaces.Space):
        return False
    
    if not isinstance(space, (spaces.Box, spaces.Discrete, spaces.MultiDiscrete, spaces.MultiBinary, spaces.Tuple, spaces.Dict)):
        return False
    
    return True

def validate_action_space(space: Union[Any, Dict]) -> bool:
    """
    Validate that the action space is of a supported type.
    
    Args:
        space: The action space to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        import gym
        from gym import spaces
    except ImportError:
        logger.warning("gym not available, skipping space validation")
        return True  # Assume valid if we can't check
    
    if isinstance(space, dict):
        space = space.get('action_space', None)
        if space is None:
            return False
    
    if space is None:
        return False
    
    if not isinstance(space, spaces.Space):
        return False
    
    if not isinstance(space, (spaces.Discrete, spaces.Box, spaces.MultiDiscrete, spaces.MultiBinary, spaces.Tuple, spaces.Dict)):
        return False
    
    return True

def safe_import(module_name: str, feature_flag: bool = False) -> Any:
    """
    Safely import a module with optional feature flag support.
    
    Args:
        module_name: Name of the module to import
        feature_flag: Whether to check for feature flags
        
    Returns:
        The imported module or None if import fails
    """
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        logger.warning(f"Failed to import module {module_name}: {e}")
        return None
    
    return module