import pytest
import time
from unittest.mock import Mock, patch, MagicMock
import random
from rclpy.publisher import Publisher
from src.embodied_edge_sim.latency_model import LatencyModel

@pytest.fixture
def latency_model():
    return LatencyModel(base_latency=0.05, jitter=0.01, packet_loss_probability=0.01, max_latency=0.1)

def test_init_with_default_parameters():
    model = LatencyModel()
    assert model.base_latency == 0.0
    assert model.jitter == 0.0
    assert model.packet_loss_probability == 0.0
    assert model.max_latency == float('inf')

def test_init_with_custom_parameters():
    model = LatencyModel(base_latency=0.1, jitter=0.05, packet_loss_probability=0.2, max_latency=0.5)
    assert model.base_latency == 0.1
    assert model.jitter == 0.05
    assert model.packet_loss_probability == 0.2
    assert model.max_latency == 0.5

@patch('random.uniform')
def test_get_latency_no_jitter(mock_uniform, latency_model):
    mock_uniform.return_value = 0.0
    latency = latency_model.get_latency()
    assert latency == 0.05

@patch('random.uniform')
def test_get_latency_with_jitter(mock_uniform, latency_model):
    mock_uniform.return_value = 0.005
    latency = latency_model.get_latency()
    assert abs(latency - 0.055) < 0.001

def test_get_latency_max_latency_enforced():
    model = LatencyModel(base_latency=0.2, jitter=0.0, max_latency=0.1)
    latency = model.get_latency()
    assert latency == 0.1

def test_get_latency_no_negative_latency():
    model = LatencyModel(base_latency=0.0, jitter=0.0, max_latency=0.1)
    with patch.object(random, 'uniform', return_value=-0.05):
        latency = model.get_latency()
        assert latency == 0.0

@patch('random.random')
def test_apply_latency_packet_dropped(mock_random, latency_model):
    mock_random.return_value = 0.005
    publisher = Mock()
    msg = Mock()
    result = latency_model.apply_latency(publisher, msg, 'test_topic')
    assert result is False

@patch('random.random')
def test_apply_latency_no_delay_publish(mock_random, latency_model):
    mock_random.return_value = 0.02
    publisher = Mock()
    msg = Mock()
    latency_model.base_latency = 0.0
    latency_model.jitter = 0.0
    result = latency_model.apply_latency(publisher, msg, 'test_topic')
    assert result is True
    publisher.publish.assert_called_once_with(msg)

@patch('random.random')
@patch('threading.Thread')
def test_apply_latency_with_delay(mock_thread, mock_random, latency_model):
    mock_random.return_value = 0.02
    publisher = Mock()
    msg = Mock()
    latency_model.base_latency = 0.05
    latency_model.jitter = 0.01
    result = latency_model.apply_latency(publisher, msg, 'test_topic')
    assert result is True
    mock_thread.assert_called()

def test_apply_latency_zero_probability_zero_latency():
    model = LatencyModel(base_latency=0.0, jitter=0.0, packet_loss_probability=0.0)
    publisher = Mock()
    msg = Mock()
    result = model.apply_latency(publisher, msg, 'test_topic')
    assert result is True
    publisher.publish.assert_called_once()

def test_apply_latency_max_latency():
    model = LatencyModel(base_latency=0.15, jitter=0.0, max_latency=0.1)
    publisher = Mock()
    msg = Mock()
    with patch('threading.Thread'):
        with patch('random.random', return_value=0.05):
            result = model.apply_latency(publisher, msg, 'test_topic')
            assert result is True

def test_get_latency_consistent_with_no_jitter():
    model = LatencyModel(base_latency=0.05, jitter=0.0)
    latencies = [model.get_latency() for _ in range(10)]
    assert all(lat == 0.05 for lat in latencies)

def test_get_latency_jitter_changes_result():
    model = LatencyModel(base_latency=0.05, jitter=0.01)
    with patch('random.uniform', side_effect=[0.005, -0.003, 0.0]):
        latencies = [model.get_latency() for _ in range(3)]
        assert latencies[0] == 0.055
        assert latencies[1] == 0.047
        assert latencies[2] == 0.05

def test_apply_latency_packet_loss_edge_case():
    model = LatencyModel(packet_loss_probability=1.0)
    publisher = Mock()
    msg = Mock()
    result = model.apply_latency(publisher, msg, 'test_topic')
    assert result is False

def test_apply_latency_no_packet_loss():
    model = LatencyModel(packet_loss_probability=0.0)
    publisher = Mock()
    msg = Mock()
    result = model.apply_latency(publisher, msg, 'test_topic')
    assert result is True

def test_apply_latency_immediate_publish():
    model = LatencyModel(base_latency=0.0, jitter=0.0, packet_loss_probability=0.0)
    publisher = Mock()
    msg = Mock()
    result = model.apply_latency(publisher, msg, 'test_topic')
    assert result is True
    publisher.publish.assert_called_once_with(msg)

@patch('time.sleep')
@patch('threading.Thread')
def test_apply_latency_delayed_publish(mock_thread, mock_sleep, latency_model):
    publisher = Mock()
    msg = Mock()
    latency_model.base_latency = 0.05
    latency_model.jitter = 0.0
    result = latency_model.apply_latency(publisher, msg, 'test_topic')
    assert result is True
    mock_thread.assert_called()

def test_latency_model_lock_usage():
    model = LatencyModel()
    with patch.object(model, '_lock') as mock_lock:
        with patch('random.uniform', return_value=0.0):
            model.get_latency()
            mock_lock.__enter__.assert_called()

def test_get_latency_caps_at_max():
    model = LatencyModel(base_latency=0.15, jitter=0.0, max_latency=0.1)
    with patch('random.uniform', return_value=0.0):
        latency = model.get_latency()
        assert latency == 0.1

def test_get_latency_no_negative():
    model = LatencyModel(base_latency=-0.1, jitter=0.0, max_latency=0.1)
    with patch('random.uniform', return_value=0.0):
        latency = model.get_latency()
        assert latency >= 0.0