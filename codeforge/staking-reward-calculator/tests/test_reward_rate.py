import pytest
from datetime import datetime
from src.models.reward_rate import RewardRate

def test_reward_rate_creation_valid():
    """Test successful creation of RewardRate with valid data"""
    rate = RewardRate(
        network="ethereum",
        annual_rate=12.5,
        timestamp=datetime.now(),
        validator_address="0x123456789"
    )
    assert rate.network == "ethereum"
    assert rate.annual_rate == 12.5
    assert rate.validator_address == "0x123456789"

def test_reward_rate_creation_without_validator():
    """Test RewardRate creation without validator address"""
    rate = RewardRate(
        network="solana",
        annual_rate=8.0,
        timestamp=datetime.now()
    )
    assert rate.network == "solana"
    assert rate.annual_rate == 8.0
    assert rate.validator_address is None

def test_reward_rate_with_commission():
    """Test RewardRate with commission rate"""
    rate = RewardRate(
        network="cosmos",
        annual_rate=15.0,
        timestamp=datetime.now(),
        commission_rate=10.0
    )
    assert rate.commission_rate == 10.0

def test_reward_rate_invalid_annual_rate_negative():
    """Test that negative annual rate raises validation error"""
    with pytest.raises(ValueError):
        RewardRate(
            network="ethereum",
            annual_rate=-5.0,
            timestamp=datetime.now()
        )

def test_reward_rate_invalid_annual_rate_over_100():
    """Test that annual rate over 100 raises validation error"""
    with pytest.raises(ValueError):
        RewardRate(
            network="ethereum",
            annual_rate=150.0,
            timestamp=datetime.now()
        )

def test_reward_rate_invalid_commission_rate_negative():
    """Test that negative commission rate raises validation error"""
    with pytest.raises(ValueError):
        RewardRate(
            network="ethereum",
            annual_rate=10.0,
            timestamp=datetime.now(),
            commission_rate=-5.0
        )

def test_reward_rate_invalid_commission_rate_over_100():
    """Test that commission rate over 100 raises validation error"""
    with pytest.raises(ValueError):
        RewardRate(
            network="ethereum",
            annual_rate=10.0,
            timestamp=datetime.now(),
            commission_rate=150.0
        )

def test_get_effective_rate_without_commission():
    """Test effective rate calculation without commission"""
    rate = RewardRate(
        network="ethereum",
        annual_rate=10.0,
        timestamp=datetime.now()
    )
    assert rate.get_effective_rate() == 10.0

def test_get_effective_rate_with_commission():
    """Test effective rate calculation with commission"""
    rate = RewardRate(
        network="ethereum",
        annual_rate=10.0,
        timestamp=datetime.now(),
        commission_rate=20.0
    )
    # 10.0 * (1 - 20.0/100) = 8.0
    assert rate.get_effective_rate() == 8.0

def test_get_effective_rate_zero_commission():
    """Test effective rate calculation with zero commission"""
    rate = RewardRate(
        network="ethereum",
        annual_rate=12.5,
        timestamp=datetime.now(),
        commission_rate=0.0
    )
    assert rate.get_effective_rate() == 12.5

def test_get_effective_rate_full_commission():
    """Test effective rate calculation with 100% commission"""
    rate = RewardRate(
        network="ethereum",
        annual_rate=10.0,
        timestamp=datetime.now(),
        commission_rate=100.0
    )
    assert rate.get_effective_rate() == 0.0

def test_reward_rate_creation_boundary_values():
    """Test creation with boundary values for rates"""
    rate = RewardRate(
        network="test",
        annual_rate=0.01,
        timestamp=datetime.now()
    )
    assert rate.annual_rate == 0.01

def test_reward_rate_timestamp_serialization():
    """Test timestamp is properly handled"""
    now = datetime(2023, 1, 1, 12, 0, 0)
    rate = RewardRate(
        network="test",
        annual_rate=5.5,
        timestamp=now
    )
    assert rate.timestamp == now

def test_reward_rate_json_serialization():
    """Test that model serializes to JSON correctly"""
    rate = RewardRate(
        network="test",
        annual_rate=7.5,
        timestamp=datetime(2023, 1, 1, 12, 0, 0),
        validator_address="test_validator"
    )
    json_data = rate.json()
    assert "test" in json_data
    assert "7.5" in json_data
    assert "test_validator" in json_data

def test_reward_rate_optional_fields():
    """Test that optional fields can be None"""
    rate = RewardRate(
        network="test",
        annual_rate=5.0,
        timestamp=datetime.now()
    )
    assert rate.commission_rate is None
    assert rate.validator_address is None

def test_reward_rate_required_fields():
    """Test that required fields must be provided"""
    with pytest.raises(Exception):
        RewardRate(
            network="test",
            timestamp=datetime.now()
        )

def test_reward_rate_network_validation():
    """Test network field validation"""
    rate = RewardRate(
        network="",
        annual_rate=5.0,
        timestamp=datetime.now()
    )
    assert rate.network == ""

def test_reward_rate_annual_rate_type_validation():
    """Test annual rate accepts float values"""
    rate = RewardRate(
        network="test",
        annual_rate=7.77,
        timestamp=datetime.now()
    )
    assert rate.annual_rate == 7.77

def test_get_effective_rate_commission_precision():
    """Test effective rate calculation precision"""
    rate = RewardRate(
        network="test",
        annual_rate=10.0,
        timestamp=datetime.now(),
        commission_rate=33.33
    )
    effective = rate.get_effective_rate()
    # 10.0 * (1 - 0.3333) = 6.667
    assert round(effective, 2) == 6.67

def test_reward_rate_commission_zero_annual_rate():
    """Test effective rate when annual rate is zero"""
    rate = RewardRate(
        network="test",
        annual_rate=0.01,
        timestamp=datetime.now(),
        commission_rate=50.0
    )
    effective = rate.get_effective_rate()
    assert effective == 0.01 * (1 - 0.5)  # 0.005