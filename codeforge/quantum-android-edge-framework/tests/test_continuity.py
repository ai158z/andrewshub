import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.backend.iit.continuity import (
    ContinuityManager, maintain_continuity, transfer_awareness
)
from src.backend.quantum.nodes import Node

@pytest.fixture
def continuity_manager():
    return ContinuityManager()

@pytest.fixture
def mock_node():
    node = Mock(spec=Node)
    node.get_state.return_value = {"state": "test"}
    node.receive_state.return_value = True
    return node

def test_maintain_continuity_valid_input(continuity_manager):
    state_vector = {"a": 0.5, "b": 0.3, "c": 0.2}
    result = continuity_manager.maintain_continuity(state_vector)
    
    assert "state" in result
    assert "phi" in result
    assert "continuity_preserved" in result
    assert "timestamp" in result

def test_maintain_continuity_invalid_input(continuity_manager):
    with pytest.raises(ValueError):
        continuity_manager.maintain_continuity("invalid_input")

def test_maintain_continuity_empty_state(continuity_manager):
    state_vector = {}
    result = continuity_manager.maintain_continuity(state_vector)
    assert result["phi"] == 0.0

def test_calculate_integrated_information_normal_case(continuity_manager):
    state_vector = {"a": 0.5, "b": 0.3, "c": 0.2}
    phi = continuity_manager._calculate_integrated_information(state_vector)
    assert isinstance(phi, float)
    assert phi >= 0

def test_calculate_integrated_information_empty_state(continuity_manager):
    state_vector = {}
    phi = continuity_manager._calculate_integrated_information(state_vector)
    assert phi == 0.0

def test_verify_continuity_above_threshold(continuity_manager):
    state_vector = {"a": 0.5, "b": 0.3, "c": 0.2}
    result = continuity_manager._verify_continuity(state_vector, 0.5)
    assert result is True

def test_verify_continuity_below_threshold(continuity_manager):
    state_vector = {"a": 0.5, "b": 0.3, "c": 0.2}
    result = continuity_manager._verify_continuity(state_vector, 0.05)
    assert result is False

def test_transfer_awareness_success(continuity_manager, mock_node):
    mock_node.get_state.return_value = {"test": "state"}
    mock_node.receive_state.return_value = True
    
    result = continuity_manager.transfer_awareness(mock_node, mock_node)
    assert result is True

def test_transfer_awareness_invalid_nodes(continuity_manager):
    result = continuity_manager.transfer_awareness(None, None)
    assert result is False

def test_transfer_awareness_no_source_state(continuity_manager, mock_node):
    mock_node.get_state.return_value = None
    result = continuity_manager.transfer_awareness(mock_node, mock_node)
    assert result is False

def test_transfer_awareness_encryption_failure(continuity_manager, mock_node):
    with patch('src.backend.iit.continuity.encrypt', side_effect=Exception("Encryption failed")):
        result = continuity_manager.transfer_awareness(mock_node, mock_node)
        assert result is False

def test_calculate_cause_effect_structure_valid(continuity_manager):
    current_state = {"a": 0.6, "b": 0.4}
    past_state = {"a": 0.5, "b": 0.5}
    
    result = continuity_manager.calculate_cause_effect_structure(current_state, past_state)
    assert "cause_repertoire" in result
    assert "effect_repertoire" in result
    assert "integrated_information" in result

def test_calculate_cause_effect_structure_empty_states(continuity_manager):
    current_state = {}
    past_state = {}
    
    result = continuity_manager.calculate_cause_effect_structure(current_state, past_state)
    assert result == {}

def test_calculate_cause_effect_structure_mismatched_lengths(continuity_manager):
    current_state = {"a": 0.6, "b": 0.4, "c": 0.2}
    past_state = {"a": 0.5, "b": 0.5}
    
    result = continuity_manager.calculate_cause_effect_structure(current_state, past_state)
    assert result["cause_repertoire"]["divergence"] == 1.0

def test_calculate_cause_repertoire_valid(continuity_manager):
    current_state = {"a": 0.6, "b": 0.4}
    past_state = {"a": 0.5, "b": 0.5}
    
    result = continuity_manager._calculate_cause_repertoire(current_state, past_state)
    assert "divergence" in result
    assert "probabilities" in result

def test_calculate_effect_repertoire_valid(continuity_manager):
    current_state = {"a": 0.6, "b": 0.4}
    result = continuity_manager._calculate_effect_repertoire(current_state)
    assert "probabilities" in result
    assert "entropy" in result

def test_calculate_effect_repertoire_empty(continuity_manager):
    current_state = {}
    result = continuity_manager._calculate_effect_repertoire(current_state)
    assert result["probabilities"] == []
    assert result["entropy"] == 0.0

def test_calculate_relative_entropy_valid(continuity_manager):
    cause_rep = {"probabilities": [0.5, 0.3, 0.2]}
    effect_rep = {"probabilities": [0.4, 0.4, 0.2]}
    
    result = continuity_manager._calculate_relative_entropy(cause_rep, effect_rep)
    assert isinstance(result, float)
    assert result >= 0.0

def test_calculate_relative_entropy_empty_inputs(continuity_manager):
    cause_rep = {"probabilities": []}
    effect_rep = {"probabilities": []}
    
    result = continuity_manager._calculate_relative_entropy(cause_rep, effect_rep)
    assert result == 0.0

def test_calculate_relative_entropy_mismatched_lengths(continuity_manager):
    cause_rep = {"probabilities": [0.5, 0.3]}
    effect_rep = {"probabilities": [0.4, 0.4, 0.2]}
    
    result = continuity_manager._calculate_relative_entropy(cause_rep, effect_rep)
    assert isinstance(result, float)
    assert result >= 0.0

def test_public_interface_functions():
    with patch('src.backend.iit.continuity.continuity_manager') as mock_cm:
        mock_cm.maintain_continuity.return_value = {"test": "result"}
        mock_cm.transfer_awareness.return_value = True
        
        result = maintain_continuity({"test": 1.0})
        assert result == {"test": "result"}
        
        transfer_result = transfer_awareness(Mock(), Mock())
        assert transfer_result is True