import pytest
from src.models import StakeData, RewardRate

def test_import_stake_data():
    """Test that StakeData can be imported from the module."""
    # Test basic instantiation
    instance = StakeData(1000, 0.05, 100, 200)
    assert isinstance(instance, StakeData)

def test_import_reward_rate():
    """Test that RewardRate can be imported from the module."""
    # Test basic instantiation
    instance = RewardRate(1000, 0.05, 100, 200)
    assert isinstance(instance, RewardRate)

def test_stake_data_attributes():
    """Test that StakeData has expected attributes."""
    instance = StakeData(1000, 0.05, 100, 200)
    assert hasattr(instance, 'amount')
    assert hasattr(instance, 'apr')
    assert hasattr(instance, 'minimum_amount')
    assert hasattr(instance, 'maximum_amount')

def test_reward_rate_attributes():
    """Test that RewardRate has expected attributes."""
    instance = RewardRate(1000, 0.05, 100, 200)
    assert hasattr(instance, 'amount')
    assert hasattr(instance, 'apr')
    assert hasattr(instance, 'minimum_amount')
    assert hasattr(instance, 'maximum_amount')

def test_stake_data_equality():
    """Test StakeData equality."""
    instance1 = StakeData(1000, 0.05, 100, 200)
    instance2 = StakeData(1000, 0.05, 100, 200)
    instance3 = StakeData(1500, 0.05, 100, 200)
    
    assert instance1 == instance2
    assert instance1 != instance3

def test_reward_rate_equality():
    """Test RewardRate equality."""
    instance1 = RewardRate(1000, 0.05, 100, 200)
    instance2 = RewardRate(1000, 0.05, 100, 200)
    instance3 = RewardRate(1500, 0.05, 100, 200)
    
    assert instance1 == instance2
    assert instance1 != instance3

def test_stake_data_repr():
    """Test StakeData string representations."""
    instance = StakeData(1000, 0.05, 100, 200)
    assert 'StakeData' in repr(instance)
    assert 'StakeData' in str(instance)

def test_reward_rate_repr():
    """Test RewardRate string representations."""
    instance = RewardRate(1000, 0.05, 100, 200)
    assert 'RewardRate' in repr(instance)
    assert 'RewardRate' in str(instance)

def test_stake_data_hash():
    """Test that StakeData instances are hashable."""
    instance = StakeData(1000, 0.05, 100, 200)
    assert hash(instance) is not None

def test_reward_rate_hash():
    """Test that RewardRate instances are hashable."""
    instance = RewardRate(1000, 0.05, 100, 200)
    assert hash(instance) is not None

def test_stake_data_comparison():
    """Test StakeData comparison methods."""
    instance1 = StakeData(1000, 0.05, 100, 200)
    instance2 = StakeData(1000, 0.05, 100, 200)
    instance3 = StakeData(1500, 0.05, 100, 200)
    
    assert instance1 <= instance2
    assert instance1 >= instance2
    assert instance1 < instance3
    assert instance3 > instance1

def test_reward_rate_comparison():
    """Test RewardRate comparison methods."""
    instance1 = RewardRate(1000, 0.05, 100, 200)
    instance2 = RewardRate(1000, 0.05, 100, 200)
    instance3 = RewardRate(1500, 0.05, 100, 200)
    
    assert instance1 <= instance2
    assert instance1 >= instance2
    assert instance1 < instance3
    assert instance3 > instance1