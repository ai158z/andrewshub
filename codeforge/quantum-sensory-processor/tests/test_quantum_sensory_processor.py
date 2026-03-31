import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
from src.quantum_sensory_processor import QuantumSensoryProcessor

@pytest.fixture
def processor():
    config = {
        "sensory_dimensions": 5,
        "context_awareness": True,
        "magic_state_threshold": 0.95
    }
    return QuantumSensoryProcessor(config)

def test_init_success(processor):
    assert processor.state["initialized"] is True
    assert processor.state["processing_enabled"] is True

def test_process_sensory_data_success(processor):
    mock_data = {"sensor1": [1, 2, 3], "sensor2": [4, 5, 6]}
    
    # Mock all the component methods
    processor.context_handler.apply_context = Mock(return_value=mock_data)
    processor.sensory_integrator.integrate_sensory_data = Mock(return_value=mock_data)
    
    result = processor.process_sensory_data(mock_data)
    
    assert "error" not in result
    processor.context_handler.apply_context.assert_called_once()
    processor.sensory_integrator.integrate_sensory_data.assert_called_once()

def test_process_sensory_data_with_magic_states(processor):
    mock_data = {"sensor1": [1, 2, 3]}
    processor.state["magic_states"] = [MagicMock()]
    
    processor.context_handler.apply_context = Mock(return_value=mock_data)
    processor.sensory_integrator.integrate_sensory_data = Mock(return_value=mock_data)
    processor.magic_state_distiller.purify_states = Mock(return_value=["purified"])
    
    result = processor.process_sensory_data(mock_data)
    
    processor.magic_state_distiller.purify_states.assert_called_once()

def test_process_sensory_data_exception_handling(processor):
    processor.context_handler.apply_context.side_effect = Exception("Context error")
    
    result = processor.process_sensory_data({"test": "data"})
    
    assert "error" in result
    assert result["error"] == "Context error"

def test_resolve_ambiguity_success(processor):
    inputs = [{"type": "visual", "confidence": 0.3}]
    
    processor.sensory_integrator.resolve_conflicts = Mock(return_value=inputs)
    processor.inverse_solver.solve_inverse_problem = Mock(return_value={"resolved": True})
    processor.inverse_solver.validate_solution = Mock(return_value=True)
    
    result = processor.resolve_ambiguity(inputs)
    
    assert "error" not in result[0]

def test_resolve_ambiguity_with_inverse_solver(processor):
    inputs = [{"type": "visual", "confidence": 0.3}]
    
    # Mock components to force inverse solver usage
    processor.sensory_integrator.resolve_conflicts = Mock(return_value=[])
    processor.inverse_solver.solve_inverse_problem = Mock(return_value={"resolved": True})
    processor.inverse_solver.validate_solution = Mock(return_value=True)
    
    result = processor.resolve_ambiguity(inputs)
    
    processor.inverse_solver.solve_inverse_problem.assert_called_once()
    processor.inverse_solver.validate_solution.assert_called_once()

def test_resolve_ambiguity_exception_handling(processor):
    inputs = [{"type": "visual", "confidence": 0.3}]
    processor.sensory_integrator.resolve_conflicts.side_effect = Exception("Conflict resolution error")
    
    result = processor.resolve_ambiguity(inputs)
    
    assert "error" in result[0]

def test_get_state_success(processor):
    processor.state["last_processed_data"] = {"test": "data"}
    processor.context_handler.get_contextual_awareness = Mock(return_value={"awareness": 0.5})
    
    result = processor.get_state()
    
    assert "error" not in result
    assert "system_state" in result

def test_get_state_with_entropy(processor):
    processor.state["last_processed_data"] = {"sensory_readings": [1, 2, 3]}
    processor.context_handler.get_contextual_awareness = Mock(return_value={"awareness": 0.5})
    
    with patch('src.quantum_sensory_processor.calculate_entropy', return_value=0.75):
        result = processor.get_state()
        
        assert "entropy" in result

def test_get_state_exception_handling(processor):
    processor.context_handler.get_contextual_awareness.side_effect = Exception("State error")
    
    result = processor.get_state()
    
    assert "error" in result

def test_process_sensory_data_empty(processor):
    mock_data = {}
    
    processor.context_handler.apply_context = Mock(return_value=mock_data)
    processor.sensory_integrator.integrate_sensory_data = Mock(return_value=mock_data)
    
    result = processor.process_sensory_data(mock_data)
    
    assert "error" not in result

def test_resolve_ambiguity_empty_list(processor):
    inputs = []
    
    processor.sensory_integrator.resolve_conflicts = Mock(return_value=[])
    processor.inverse_solver.solve_inverse_problem = Mock(return_value={"resolved": True})
    processor.inverse_solver.validate_solution = Mock(return_value=True)
    
    result = processor.resolve_ambiguity(inputs)
    
    assert isinstance(result, list)

def test_resolve_ambiguity_no_ambiguity_resolution(processor):
    inputs = [{"confidence": 0.9}]
    
    processor.sensory_integrator.resolve_conflicts = Mock(return_value=[{"confidence": 0.9}])
    processor.inverse_solver.solve_inverse_problem = Mock(return_value={"resolved": True})
    processor.inverse_solver.validate_solution = Mock(return_value=True)
    
    result = processor.resolve_ambiguity(inputs)
    
    processor.inverse_solver.solve_inverse_problem.assert_not_called()

def test_get_state_no_last_data(processor):
    result = processor.get_state()
    
    assert "last_processed_data" in result

@pytest.mark.parametrize("input_data,expected", [
    ({"a": 1}, {"a": 1}),
    ({"b": 2}, {"b": 2}),
])
def test_process_sensory_data_parametrized(processor, input_data, expected):
    processor.context_handler.apply_context = Mock(return_value=input_data)
    processor.sensory_integrator.integrate_sensory_data = Mock(return_value=expected)
    
    result = processor.process_sensory_data(input_data)
    
    assert result == expected

def test_process_sensory_data_with_context(processor):
    mock_data = {"sensor": [1, 2]}
    
    processor.context_handler.apply_context = Mock(return_value=mock_data)
    processor.sensory_integrator.integrate_sensory_data = Mock(return_value=mock_data)
    
    result = processor.process_sensory_data(mock_data)
    
    processor.context_handler.apply_context.assert_called_with(mock_data, "default")

def test_calculate_entropy_called(processor):
    mock_data = {"sensory_readings": [0.5, 0.3, 0.2]}
    
    processor.context_handler.apply_context = Mock(return_value=mock_data)
    processor.sensory_integrator.integrate_sensory_data = Mock(return_value=mock_data)
    
    with patch('src.quantum_sensory_processor.calculate_entropy', return_value=0.5) as mock_entropy:
        result = processor.process_sensory_data(mock_data)
        
        mock_entropy.assert_called()

def test_resolve_ambiguity_inverse_solver_validation_fails(processor):
    inputs = [{"type": "visual", "confidence": 0.3}]
    
    processor.sensory_integrator.resolve_conflicts = Mock(return_value=[])
    processor.inverse_solver.solve_inverse_problem = Mock(return_value={"resolved": False})
    processor.inverse_solver.validate_solution = Mock(return_value=False)
    
    result = processor.resolve_ambiguity(inputs)
    
    assert len(result) == 0

def test_get_state_with_no_context_awareness(processor):
    processor.context_handler.get_contextual_awareness = Mock(return_value={})
    
    result = processor.get_state()
    
    processor.context_handler.get_contextual_awareness.assert_called_once()

def test_process_sensory_data_integration_error(processor):
    mock_data = {"sensor": [1, 2]}
    
    processor.context_handler.apply_context = Mock(return_value=mock_data)
    processor.sensory_integrator.integrate_sensory_data = Mock(side_effect=Exception("Integration error"))
    
    result = processor.process_sensory_data(mock_data)
    
    assert "error" in result
    assert result["error"] == "Integration error"