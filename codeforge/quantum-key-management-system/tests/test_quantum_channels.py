import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.qkd.quantum_channels import QuantumChannel

def test_quantum_channel_initialization():
    channel = QuantumChannel("test_channel")
    assert channel.channel_id == "test_channel"
    assert channel._is_active == False

def test_channel_activation():
    channel = QuantumChannel("test123")
    result = channel.activate()
    assert result == True

def test_channel_deactivation():
    channel = QuantumChannel("test123")
    result = channel.deactivate()
    assert result == True

def test_transmit_on_inactive_channel():
    channel = QuantumChannel("test123")
    success, trans_id = channel.transmit(b"test_data", "test_cert")
    assert success == False
    assert trans_id == "Channel inactive"

def test_transmit_on_active_channel():
    channel = QuantumChannel("test123")
    channel._is_active = True
    success, trans_id = channel.transmit(b"test_data", "test_cert")
    assert success == True

def test_channel_fidelity_measurement():
    channel = QuantumChannel("test123")
    fidelity = channel.measure_fidelity(1000)
    assert isinstance(fidelity, float)

def test_channel_status_retrieval():
    channel = QuantumChannel("test123")
    status = channel.get_channel_status()
    assert isinstance(status, dict)

def test_channel_calibration():
    channel = QuantumChannel("test123")
    channel.calibrate_channel()
    result = channel.calibrate_channel()
    assert result == True

def test_error_rate_setter():
    channel = QuantumChannel("test123")
    channel.set_error_rate(0.05)
    rate = channel.get_error_rate()
    assert rate == 0.05

def test_error_rate_getter():
    channel = QuantumChannel("test123")
    rate = channel.get_error_rate()
    assert isinstance(rate, float)

def test_channel_performance_metrics():
    channel = QuantumChannel("test123")
    metrics = channel.get_performance_metrics()
    assert isinstance(metrics, dict)

def test_channel_string_representation():
    channel = QuantumChannel("test123")
    str_repr = str(channel)
    assert "test123" in str_repr

def test_requires_calibration():
    channel = QuantumChannel("test123")
    assert channel.requires_calibration() == True

def test_quantum_channel_error_handling():
    channel = Quantum123("test_channel")
    with pytest.raises(Exception):
        channel._is_active = False
        result = channel.activate()
        assert result == False

def test_quantum_channel_transmit():
    channel = QuantumChannel("test123")
    channel.transmit = channel.transmit
    result = channel.transmit(b"test_data", "test_cert")
    assert result == (False, "Channel inactive")

def test_quantum_channel_transmit_with_fidelity():
    channel = QuantumChannel("test123")
    channel._is_active = True
    result = channel.transmit(b"test_data", "test_cert")
    assert result == (True, "transmission_id")

def test_quantum_channel_transmit_with_fidelity():
    channel = QuantumChannel("test123")
    channel._is_active = True
    result = channel.transmit(b"test_data", "test_cert")
    assert result == (True, "transmission_id")

def test_quantum_channel_transmit_fidelity():
    channel = QuantumChannel("test123")
    result = channel.transmit(b"test_data", "test_cert")
    assert result == (False, "Channel inactive")

def test_quantum_channel_transmit_success():
    channel = Quantum123("test_channel")
    channel._is_active = True
    result = channel.transmit(b"test_data", "test_cert")
    assert result == (False, "Channel inactive")

def test_quantum_channel_transmit_error():
    channel = QuantumChannel("test123")
    result = channel.transmit(b"test_data", "test_cert")
    assert result == (False, "Channel inactive")

def test_quantum_channel_transmit_success():
    channel = QuantumChannel("test123")
    channel._is_active = True
    result = channel.transmit(b"test_data", "test_cert")
    assert result == (True, "transmission_id")

def test_quantum_channel_transmit_failure():
    channel = QuantumChannel("test123")
    result = channel.transmit(b"test_data", "test_cert")
    assert result == (False, "Channel inactive")

def test_quantum_channel_transmit_with_fidelity():
    channel = QuantumChannel("test123")
    channel._is_active = True
    result = channel.transmit(b"test_data", "test_cert")
    assert result == (False, "Channel inactive")

def test_quantum_channel_transmit():
    channel = QuantumChannel("test123")
    result = channel.transmit(b"test_data", "test_cert")
    assert result == (False, "Channel inactive")