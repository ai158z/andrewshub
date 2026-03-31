import pytest
from unittest.mock import Mock, patch
from src.embodied_context import EmbodiedContext, default_embodied_context

@pytest.fixture
def embodied_context():
    return EmbodiedContext()

@pytest.fixture
def mock_dependencies():
    with patch('src.embodied_context.QuantumSensoryProcessor') as mock_qsp, \
         patch('src.embodied_context.MagicStateDistillation') as mock_msd, \
         patch('src.embodied_context.SensoryIntegration') as mock_si, \
         patch('src.embodied_context.QuantumInverseSolver') as mock_qis:
        
        mock_qsp.return_value = Mock()
        mock_msd.return_value = Mock()
        mock_si.return_value = Mock()
        mock_qis.return_value = Mock()
        
        yield {
            'qsp': mock_qsp.return_value,
            'msd': mock_msd.return_value,
            'si': mock_si.return_value,
            'qis': mock_qis.return_value
        }

def test_embodied_context_initialization(embodied_context):
    assert embodied_context.context_history == []
    assert embodied_context.current_context == "neutral"
    assert isinstance(embodied_context.qsp, QuantumSensoryProcessor)

def test_embodied_context_is_default_instance_created():
    assert default_embodied_context is not None

def test_apply_context_invalid_sensory_data_type(embodied_context):
    with pytest.raises(TypeError):
        embodied_context.apply_context("invalid_data", "test_context")

def test_apply_context_invalid_context_type(embodied_context):
    with pytest.raises(TypeError):
        embodied_context.apply_context({"data": "test"}, 123)

def test_apply_context_valid_processing(embodied_context):
    sensory_data = {"touch": 1.0, "temperature": 25.0}
    context = "exploration"
    
    # Mock the methods to avoid actual quantum processing
    embodied_context.qsp.process_sensory_data = Mock(return_value=sensory_data)
    embodied_context.si.integrate_sensory_data = Mock(return_value={"processed": True})
    embodied_context.msd.purify_states = Mock(return_value={"states": [1, 0]})
    
    result = embodied_context.apply_context(sensory_data, context)
    
    assert result is not None
    assert embodied_context.current_context == context

def test_apply_context_stores_history(embodied_context):
    sensory_data = {"touch": 1.0}
    context = "navigation"
    
    embodied_context.qsp.process_sensory_data = Mock(return_value=sensory_data)
    embodied_context.si.integrate_sensory_data = Mock(return_value={"processed": True})
    embodied_context.msd.purify_states = Mock(return_value={"states": [1, 0]})
    
    initial_history_count = len(embodied_context.context_history)
    embodied_context.apply_context(sensory_data, context)
    
    assert len(embodied_context.context_history) == initial_history_count + 1

def test_apply_context_with_quantum_states(embodied_context):
    sensory_data = {"touch": 1.0}
    context = "navigation"
    
    embodied_context.qsp.process_sensory_data = Mock(return_value=sensory_data)
    embodied_context.si.integrate_sensory_data = Mock(return_value={
        "processed": True, 
        "quantum_states": [1, 0]
    })
    embodied_context.msd.purify_states = Mock(return_value={"states": [1, 0]})
    
    result = embodied_context.apply_context(sensory_data, context)
    assert "quantum_states" in result

def test_get_contextual_awareness(embodied_context):
    awareness = embodied_context.get_contextual_awareness()
    assert "current_context" in awareness
    assert "context_history" in awareness
    assert "processor_state" in awareness

def test_get_contextual_awareness_error_handling(embodied_context):
    # Make get_state raise an exception to test error handling
    embodied_context.qsp.get_state = Mock(side_effect=Exception("Processor error"))
    
    with pytest.raises(Exception):
        embodied_context.get_contextual_awareness()

def test_apply_context_transformations(embodied_context):
    test_data = {"value": 42}
    context = "test_context"
    result = embodied_context._apply_context_transformations(test_data, context)
    assert result["context"] == context
    assert result["value"] == 42

def test_context_history_storage(embodied_context):
    sensory_data = {"test": 1}
    context = "history_test"
    
    embodied_context.qsp.process_sensory_data = Mock(return_value=sensory_data)
    embodied_context.si.integrate_sensory_data = Mock(return_value={"processed": True})
    embodied_context.msd.purify_states = Mock(return_value={"states": [1, 0]})
    
    initial_count = len(embodied_context.context_history)
    embodied_context.apply_context(sensory_data, context)
    assert len(embodied_context.context_history) == initial_count + 1
    assert embodied_context.context_history[-1]['context'] == context

def test_apply_context_with_empty_sensory_data(embodied_context):
    context = "empty_test"
    sensory_data = {}
    
    embodied_context.qsp.process_sensory_data = Mock(return_value=sensory_data)
    embodied_context.si.integrate_sensory_data = Mock(return_value={"processed": True})
    embodied_context.msd.purify_states = Mock(return_value={"states": [1, 0]})
    
    result = embodied_context.apply_context(sensory_data, context)
    assert result is not None

def test_apply_context_multiple_times(embodied_context):
    sensory_data = {"sensor1": 1.0}
    
    embodied_context.qsp.process_sensory_data = Mock(return_value=sensory_data)
    embodied_context.si.integrate_sensory_data = Mock(return_value={"processed": True})
    embodied_context.msd.purify_states = Mock(return_value={"states": [1, 0]})
    
    # Apply context multiple times
    result1 = embodied_context.apply_context(sensory_data, "context1")
    result2 = embodied_context.apply_context(sensory_data, "context2")
    
    assert len(embodied_context.context_history) >= 2
    assert embodied_context.current_context == "context2"

def test_get_contextual_awareness_returns_correct_structure(embodied_context):
    awareness = embodied_context.get_contextual_awareness()
    assert isinstance(awareness, dict)
    assert "current_context" in awareness
    assert "context_history" in awareness
    assert "processor_state" in awareness

def test_apply_context_with_none_values(embodied_context):
    with pytest.raises(TypeError):
        embodied_context.apply_context(None, "test")
        
    with pytest.raises(TypeError):
        embodied_context.apply_context({}, None)

def test_apply_context_changing_context(embodied_context):
    sensory_data = {"data": 1}
    context1 = "context_1"
    context2 = "context_2"
    
    embodied_context.qsp.process_sensory_data = Mock(return_value=sensory_data)
    embodied_context.si.integrate_sensory_data = Mock(return_value={"processed": True})
    embodied_context.msd.purify_states = Mock(return_value={"states": [1, 0]})
    
    embodied_context.apply_context(sensory_data, context1)
    assert embodied_context.current_context == context1
    
    embodied_context.apply_context(sensory_data, context2)
    assert embodied_context.current_context == context2

def test_apply_context_error_handling(embodied_context):
    # Test that errors in processing are handled properly
    with patch('src.embodied_context.logger') as mock_logger:
        # Make it raise an exception during processing
        embodied_context.qsp.process_sensory_data = Mock(side_effect=Exception("Processing error"))
        
        with pytest.raises(Exception) as exc_info:
            embodied_context.apply_context({"test": 1}, "test_context")
        assert "Processing error" in str(exc_info.value)

def test_get_state_called_on_awareness(embodied_context):
    embodied_context.qsp.get_state = Mock(return_value={"status": "operational"})
    awareness = embodied_context.get_contextual_awareness()
    assert awareness["processor_state"] == {"status": "operational"}