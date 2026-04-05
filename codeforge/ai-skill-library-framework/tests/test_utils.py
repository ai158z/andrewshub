import gym
from gym import spaces
import numpy as np
from src.utils import validate_observation_space, validate_action_space, safe_import

def test_validate_observation_space_with_valid_box_space():
    space = spaces.Box(low=-1, high=1, shape=(4,))
    assert validate_observation_space(space) is True

def test_validate_observation_space_with_valid_discrete_space():
    space = spaces.Discrete(5)
    assert validate_observation_space(space) is True

def test_validate_observation_space_with_invalid_type():
    space = "invalid_space_type"
    assert validate_observation_space(space) is False

def test_validate_observation_space_with_unsupported_space_type():
    class UnsupportedSpace(gym.Space):
        def __init__(self):
            super().__init__()
    space = UnsupportedSpace()
    assert validate_observation_space(space) is False

def test_validate_observation_space_with_dict_containing_valid_space():
    space = {'observation_space': spaces.Box(low=-1, high=1, shape=(4,))}
    assert validate_observation_space(space) is True

def test_validate_observation_space_with_dict_missing_observation_space():
    space = {'action_space': spaces.Discrete(2)}
    assert validate_observation_space(space) is False

def test_validate_action_space_with_valid_discrete_space():
    space = spaces.Discrete(4)
    assert validate_action_space(space) is True

def test_validate_action_space_with_valid_box_space():
    space = spaces.Box(low=-1, high=1, shape=(2,))
    assert validate_action_space(space) is True

def test_validate_action_space_with_invalid_type():
    space = "invalid_space_type"
    assert validate_action_space(space) is False

def test_validate_action_space_with_unsupported_space_type():
    class UnsupportedSpace(gym.Space):
        def __init__(self):
            super().__init__()
    space = UnsupportedSpace()
    assert validate_action_space(space) is False

def test_validate_action_space_with_dict_containing_valid_space():
    space = {'action_space': spaces.Discrete(2)}
    assert validate_action_space(space) is True

def test_validate_action_space_with_dict_missing_action_space():
    space = {'observation_space': spaces.Box(low=-1, high=1, shape=(4,))}
    assert validate_action_space(space) is False

def test_safe_import_with_valid_module():
    module = safe_import('gym')
    assert module is not None
    assert module.__name__ == 'gym'

def test_safe_import_with_invalid_module():
    module = safe_import('nonexistent_module')
    assert module is None

def test_safe_import_with_feature_flag():
    module = safe_import('gym', feature_flag=True)
    assert module is not None
    assert module.__name__ == 'gym'

def test_validate_observation_space_with_none():
    assert validate_observation_space(None) is False

def test_validate_action_space_with_none():
    assert validate_action_space(None) is False

def test_validate_observation_space_with_multi_discrete():
    space = spaces.MultiDiscrete([2, 3])
    assert validate_observation_space(space) is True

def test_validate_action_space_with_multi_binary():
    space = spaces.MultiBinary(4)
    assert validate_action_space(space) is True