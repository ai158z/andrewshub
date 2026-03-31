import json
import numpy as np
import pytest
from unittest.mock import mock_open, patch, MagicMock
from codonic_layer.persistence import StatePersistence
from codonic_layer.quantum_states import QuantumStates

@pytest.fixture
def state_persistence():
    return StatePersistence()

@pytest.fixture
def sample_state_data():
    return {
        'amplitudes': np.array([1, 2, 3]),
        'metadata': {'key': 'value'},
        'state_vector': np.array([0.5, 0.5, 0.5, 0.5])
    }

def test_save_state_success(state_persistence, sample_state_data):
    with patch("builtins.open", mock_open()) as mock_file:
        with patch("json.dumps") as mock_dumps:
            mock_dumps.return_value = '{"amplitudes": [1, 2, 3]}'
            result = state_persistence.save_state(sample_state_data)
            assert result is True

def test_save_state_file_error_handling(state_persistence, sample_state_data):
    with patch("builtins.open", side_effect=Exception("File error")):
        result = state_persistence.save_state(sample_state_data)
        assert result is False

def test_load_state_success(state_persistence):
    mock_data = '{"amplitudes": [1, 2, 3], "metadata": {"key": "value"}}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = state_persistence.load_state()
        assert result is not None

def test_load_state_file_not_found(state_persistence):
    with patch("builtins.open", side_effect=FileNotFoundError()):
        result = state_persistence.load_state()
        assert result is None

def test_serialize_quantum_state_with_numpy_arrays(state_persistence, sample_state_data):
    result = state_persistence.serialize_quantum_state(sample_state_data)
    assert isinstance(result, str)
    loaded = json.loads(result)
    assert isinstance(loaded['amplitudes'], list)

def test_serialize_quantum_state_with_nested_dict_containing_arrays(state_persistence):
    state_data = {
        'nested': {
            'vector': np.array([1, 2, 3])
        }
    }
    result = state_persistence.serialize_quantum_state(state_data)
    assert isinstance(result, str)
    loaded = json.loads(result)
    assert isinstance(loaded['nested']['vector'], list)

def test_deserialize_quantum_state_with_arrays(state_persistence):
    data = '{"amplitudes": [1, 2, 3], "metadata": {"key": "value"}}'
    result = state_persistence.deserialize_quantum_state(data)
    assert isinstance(result['amplitudes'], np.ndarray)

def test_deserialize_quantum_state_with_non_array_data(state_persistence):
    data = '{"key": "value", "metadata": "simple_string"}'
    result = state_persistence.deserialize_quantum_state(data)
    assert result['key'] == 'value'

def test_deserialize_quantum_state_empty_data(state_persistence):
    data = '{}'
    result = state_persistence.deserialize_quantum_state(data)
    assert result == {}

def test_serialize_quantum_state_serializes_arrays(state_persistence):
    state_data = {
        'array': np.array([1, 2, 3]),
        'simple': 'value'
    }
    result = state_persistence.serialize_quantum_state(state_data)
    assert '"array": [1, 2, 3]' in result

def test_serialize_quantum_state_serializes_nested_arrays(state_persistence):
    state_data = {
        'nested': {'inner': np.array([4, 5, 6])}
    }
    result = state_persistence.serialize_quantum_state(state_data)
    assert '"inner": [4, 5, 6]' in result

def test_deserialize_quantum_state_converts_lists_to_arrays(state_persistence):
    data = '{"simple_list": [1, 2, 3], "text": "value"}'
    result = state_persistence.deserialize_quantum_state(data)
    assert isinstance(result['simple_list'], np.ndarray)

def test_backup_state_success(state_persistence):
    mock_state = MagicMock()
    mock_state.get_state.return_value = np.array([0.5, 0.5, 0.5])
    
    with patch("builtins.open", mock_open()) as mock_file:
        result = state_persistence.backup_state(mock_state, "backup.json")
        assert result is True

def test_backup_state_handles_exception(state_persistence):
    mock_state = MagicMock()
    mock_state.get_state.side_effect = Exception("State error")
    
    result = state_persistence.backup_state(mock_state, "backup.json")
    assert result is False

def test_save_state_custom_filepath(state_persistence, sample_state_data):
    with patch("builtins.open", mock_open()) as mock_file:
        state_persistence.save_state(sample_state_data, "custom_path.json")
        # The mock checks if file was opened with the right path
        mock_file.assert_called_with("custom_path.json", "w")

def test_load_state_custom_filepath(state_persistence):
    mock_data = '{"key": "value"}'
    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
        state_persistence.load_state("custom_path.json")
        mock_file.assert_called_with("custom_path.json", "r")

def test_serialize_handles_empty_dict(state_persistence):
    result = state_persistence.serialize_quantum_state({})
    assert result == '{}'

def test_deserialize_handles_empty_string(state_persistence):
    result = state_persistence.deserialize_quantum_state('{}')
    assert result == {}

def test_serialize_handles_none_values(state_persistence):
    data = {'null_value': None, 'array': np.array([1,2,3])}
    result = state_persistence.serialize_quantum_state(data)
    assert 'null_value' in result

def test_deserialize_maintains_non_array_types(state_persistence):
    data = '{"text": "value", "number": 42, "flag": true}'
    result = state_persistence.deserialize_quantum_state(data)
    assert result == {'text': 'value', 'number': 42, 'flag': True}