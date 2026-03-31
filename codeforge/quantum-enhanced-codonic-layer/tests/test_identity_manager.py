import pytest
import numpy as np
from unittest.mock import Mock, patch, mock_open
from codonic_layer.identity_manager import IdentityManager

@pytest.fixture
def identity_manager():
    return IdentityManager()

@pytest.fixture
def sample_identity_data():
    return {
        "identity_id": "test-123",
        "quantum_state": {"state": "test"},
        "created_at": 1234567890.0,
        "updated_at": 1234567890.0,
        "metadata": {"version": "1.0"}
    }

def test_init_creates_persistence_dir():
    with patch('os.makedirs') as mock_makedirs:
        manager = IdentityManager("./test_dir")
        mock_makedirs.assert_called_with("./test_dir", exist_ok=True)

def test_create_identity_success(identity_manager):
    with patch.object(identity_manager, 'save_identity') as mock_save:
        result = identity_manager.create_identity("test-id")
        mock_save.assert_called_once()
        assert result is not None
        assert "identity_id" in result

def test_create_identity_with_quantum_states(identity_manager):
    with patch('codonic_layer.identity_manager.QuantumStates') as mock_quantum_states:
        mock_instance = Mock()
        mock_quantum_states.return_value = mock_instance
        mock_instance.get_state.return_value = {"test": "state"}
        result = identity_manager.create_identity("test-id")
        assert result is not None

def test_load_identity_success(identity_manager):
    mock_data = {"identity_id": "test-id", "data": "test"}
    with patch('os.path.exists', return_value=True):
        with patch.object(identity_manager.state_persistence, 'load_state', return_value=mock_data):
            result = identity_manager.load_identity("test-id")
            assert result == mock_data

def test_load_identity_not_found(identity_manager):
    with patch('os.path.exists', return_value=False):
        result = identity_manager.load_identity("test-id")
        assert result is None

def test_update_identity_success(identity_manager, sample_identity_data):
    with patch.object(identity_manager, 'load_identity', return_value=sample_identity_data):
        with patch.object(identity_manager, 'save_identity', return_value=True):
            result = identity_manager.update_identity("test-id", {"new_field": "value"})
            assert result is True

def test_update_identity_not_found(identity_manager):
    with patch.object(identity_manager, 'load_identity', return_value=None):
        result = identity_manager.update_identity("test-id", {"new_field": "value"})
        assert result is False

def test_get_identity_state_success(identity_manager, sample_identity_data):
    with patch.object(identity_manager, 'load_identity', return_value=sample_identity_data):
        result = identity_manager.get_identity_state("test-id")
        assert result is not None
        assert result["identity_id"] == "test-id"

def test_get_identity_state_not_found(identity_manager):
    with patch.object(identity_manager, 'load_identity', return_value=None):
        result = identity_manager.get_identity_state("test-id")
        assert result is None

def test_save_identity_success(identity_manager, sample_identity_data):
    with patch.object(identity_manager.state_persistence, 'save_state', return_value=True):
        with patch('codonic_layer.identity_manager.normalize_state', return_value={"normalized": True}):
            result = identity_manager.save_identity("test-id", sample_identity_data)
            assert result is True

def test_save_identity_failure(identity_manager, sample_identity_data):
    with patch.object(identity_manager.state_persistence, 'save_state', return_value=False):
        result = identity_manager.save_identity("test-id", sample_identity_data)
        assert result is False

def test_create_identity_exception_handling(identity_manager):
    with patch.object(identity_manager.state_persistence, 'save_state', side_effect=Exception("Test error")):
        with pytest.raises(Exception):
            identity_manager.create_identity("test-id")

def test_load_identity_exception_handling(identity_manager):
    with patch('os.path.exists', side_effect=Exception("Load error")):
        with pytest.raises(Exception):
            identity_manager.load_identity("test-id")

def test_update_identity_exception_handling(identity_manager):
    with patch.object(identity_manager, 'load_identity', side_effect=Exception("Update error")):
        with pytest.raises(Exception):
            identity_manager.update_identity("test-id", {})

def test_get_identity_state_exception_handling(identity_manager):
    with patch.object(identity_manager, 'load_identity', side_effect=Exception("State error")):
        with pytest.raises(Exception):
            identity_manager.get_identity_state("test-id")

def test_create_identity_with_persistence_error(identity_manager):
    with patch.object(identity_manager, 'save_identity', return_value=False):
        result = identity_manager.create_identity("test-id")
        assert result is not None

def test_update_identity_with_persistence_error(identity_manager):
    with patch.object(identity_manager, 'save_identity', return_value=False):
        result = identity_manager.update_identity("test-id", {})
        assert result is False

def test_load_identity_with_persistence_error(identity_manager):
    with patch.object(identity_manager.state_persistence, 'load_state', return_value=None):
        result = identity_manager.load_identity("test-id")
        assert result is None

def test_get_identity_state_with_load_error(identity_manager):
    with patch.object(identity_manager, 'load_identity', return_value=None):
        result = identity_manager.get_identity_state("test-id")
        assert result is None