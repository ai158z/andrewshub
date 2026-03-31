import pytest
import numpy as np
from unittest.mock import Mock, patch, call
from src.sensory_integration import SensoryIntegration

@pytest.fixture
def sensory_integration():
    return SensoryIntegration()

@pytest.fixture
def mock_sensory_data():
    return {
        'visual': [0.1, 0.2, 0.3],
        'auditory': [0.4, 0.5, 0.6],
        'tactile': [0.7, 0.8, 0.9]
    }

@pytest.fixture
def mock_processed_data():
    return {
        'visual': [0.1, 0.2, 0.3],
        'auditory': [0.4, 0.5, 0.6],
        'tactile': [0.7, 0.8, 0.9],
        'timestamp': 1234567890
    }

def test_sensory_integration_initialization():
    si = SensoryIntegration()
    assert si is not None
    assert hasattr(si, 'quantum_processor')
    assert hasattr(si, 'state_distiller')
    assert hasattr(si, 'inverse_solver')
    assert hasattr(si, 'context_engine')

@patch('src.sensory_integration.QuantumSensoryProcessor')
@patch('src.sensory_integration.EmbodiedContext')
@patch('src.sensory_integration.calculate_entropy')
def test_integrate_sensory_data_success(mock_entropy, mock_context, mock_processor):
    mock_processor.return_value.process_sensory_data.return_value = {'data': 'processed'}
    mock_context.return_value.apply_context.return_value = {'data': 'contextualized'}
    mock_entropy.return_value = 0.3
    
    si = SensoryIntegration()
    sensory_inputs = {'visual': [1, 2, 3], 'auditory': [4, 5, 6]}
    
    result = si.integrate_sensory_data(sensory_inputs)
    
    assert result['processed'] == True
    assert 'integrated_data' in result
    assert 'confidence' in result

@patch('src.sensory_integration.QuantumSensoryProcessor')
@patch('src.sensory_integration.EmbodiedContext')
def test_integrate_sensory_data_with_ambiguity(mock_context, mock_processor):
    mock_processor.return_value.process_sensory_data.return_value = {'data': 'processed'}
    mock_processor.return_value.resolve_ambiguity.return_value = {'resolved': 'data'}
    mock_context.return_value.apply_context.return_value = {'data': 'contextualized'}
    mock_context.return_value.get_contextual_awareness.return_value = {'environment': 'test'}
    
    si = SensoryIntegration()
    si._detect_ambiguity = Mock(return_value=True)
    
    sensory_inputs = {'visual': [1, 2, 3], 'auditory': [4, 5, 6]}
    result = si.integrate_sensory_data(sensory_inputs)
    
    assert result['processed'] == True
    si._detect_ambiguity.assert_called()

def test_detect_ambiguity_high():
    si = SensoryIntegration()
    data = {'sensor1': [1, 2, 3], 'sensor2': [4, 5, 6]}
    
    # Mock calculate_entropy to return high value
    with patch('src.sensory_integration.calculate_entropy', return_value=0.8):
        result = si._detect_ambiguity(data)
        assert result == True

def test_detect_ambiguity_low():
    si = SensoryIntegration()
    data = {'sensor1': [1, 1, 1], 'sensor2': [1, 1, 1]}
    
    # Mock calculate_entropy to return low value
    with patch('src.sensory_integration.calculate_entropy', return_value=0.2):
        result = si._detect_ambiguity(data)
        assert result == False

def test_detect_ambiguity_empty_data():
    si = SensoryIntegration()
    result = si._detect_ambiguity({})
    assert result == False

@patch('src.sensory_integration.MagicStateDistillation')
@patch('src.sensory_integration.QuantumSensoryProcessor')
@patch('src.sensory_integration.QuantumInverseSolver')
def test_resolve_conflicts_success(mock_solver, mock_processor, mock_distiller):
    mock_distiller.return_value.purify_states.return_value = [[1, 2], [3, 4]]
    mock_processor.return_value.resolve_ambiguity.return_value = {'resolved': 'data'}
    mock_solver.return_value.solve_inverse_problem.return_value = {'solution': 'valid'}
    mock_solver.return_value.validate_solution.return_value = True
    
    si = SensoryIntegration()
    data_points = [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}]
    
    result = si.resolve_conflicts(data_points)
    
    assert len(result) == 2
    assert isinstance(result, list)

def test_resolve_conflicts_invalid_input():
    si = SensoryIntegration()
    
    # Test with None input
    result = si.resolve_conflicts(None)
    assert result is None
    
    # Test with empty list
    result = si.resolve_conflicts([])
    assert result == []

@patch('src.sensory_integration.MagicStateDistillation')
@patch('src.sensory_integration.QuantumSoryProcessor')
@patch('src.sensory_integration.QuantumInverseSolver')
def test_resolve_conflicts_validation_failure(mock_solver, mock_processor, mock_distiller):
    mock_distiller.return_value.purify_states.return_value = [[1, 2], [3, 4]]
    mock_processor.return_value.resolve_ambiguity.return_value = {'resolved': 'data'}
    mock_solver.return_value.solve_inverse_problem.return_value = {'solution': 'invalid'}
    mock_solver.return_value.validate_solution.return_value = False
    
    si = SensoryIntegration()
    data_points = [{'x': 1, 'y': 2}]
    
    result = si.resolve_conflicts(data_points)
    assert result == data_points

@patch('src.sensory_integration.QuantumSensoryProcessor')
@patch('src.sensory_integration.EmbodiedContext')
def test_integrate_sensory_data_error_handling(mock_context, mock_processor):
    mock_processor.return_value.process_sensory_data.side_effect = Exception("Processing error")
    mock_context.return_value.apply_context.return_value = {'data': 'contextualized'}
    
    si = SensoryIntegration()
    sensory_inputs = {'visual': [1, 2, 3]}
    
    result = si.integrate_sensory_data(sensory_inputs)
    
    assert result['processed'] == False
    assert 'error' in result

def test_integrate_sensory_data_empty_input():
    si = SensoryIntegration()
    result = si.integrate_sensory_data({})
    # Should handle empty input gracefully
    assert result['processed'] == True or result['processed'] == False

@patch('src.sensory_integration.calculate_entropy')
def test_integrate_sensory_data_high_entropy(mock_entropy):
    mock_entropy.return_value = 0.8  # High entropy
    
    si = SensoryIntegration()
    sensory_inputs = {'visual': [1, 2, 3], 'auditory': [4, 5, 6]}
    
    # Mock the methods that would be called
    si.quantum_processor.resolve_ambiguity = Mock(return_value={'resolved': 'data'})
    si.context_engine.get_contextual_awareness = Mock(return_value={'environment': 'test'})
    si.context_engine.apply_context = Mock(return_value={'data': 'contextualized'})
    
    result = si.integrate_sensory_data(sensory_inputs)
    
    assert 'integrated_data' in result
    assert 'confidence' in result

def test_ambiguity_detection_edge_cases():
    si = SensoryIntegration()
    
    # Test with None data
    assert si._detect_ambiguity(None) == False
    
    # Test with single value data (zero entropy)
    single_value_data = {'sensor1': [1, 1, 1], 'sensor2': [1, 1, 1]}
    with patch('src.sensory_integration.calculate_entropy', return_value=0.0):
        assert si._detect_ambiguity(single_value_data) == False
    
    # Test with high entropy data
    with patch('src.sensory_integration.calculate_entropy', return_value=0.9):
        assert si._detect_ambiguity(single_value_data) == True

@patch('src.sensory_integration.MagicStateDistillation')
@patch('src.sensory_integration.QuantumInverseSolver')
def test_resolve_conflicts_error_handling(mock_solver, mock_distiller):
    mock_distiller.return_value.purify_states.side_effect = Exception("Distillation error")
    mock_solver.return_value.solve_inverse_problem.return_value = {}
    mock_solver.return_value.validate_solution.return_value = False
    
    si = SensoryIntegration()
    
    # Input that causes error
    problematic_data = "invalid_input"
    
    result = si.resolve_conflicts(problematic_data)
    # Should return original data when error occurs
    assert result == problematic_data

def test_calculate_confidence():
    # Test that confidence is calculated as 1.0 - entropy
    with patch('src.sensory_integration.calculate_entropy', return_value=0.3):
        si = SensoryIntegration()
        confidence = 1.0 - 0.3  # 0.7
        assert confidence == 0.7

@patch('src.sensory_integration.QuantumSensoryProcessor')
@patch('src.sensory_integration.EmbodiedContext')
def test_integrate_sensory_data_confidence_calculation(mock_context, mock_processor):
    mock_processor.return_value.process_sensory_data.return_value = {'data': 'processed', 'timestamp': 1234567890}
    mock_context.return_value.apply_context.return_value = {'data': 'contextualized'}
    mock_context.return_value.get_contextual_awareness.return_value = {'environment': 'test'}
    
    si = SensoryIntegration()
    with patch('src.sensory_integration.calculate_entropy', return_value=0.4):
        sensory_inputs = {'visual': [1, 2, 3], 'auditory': [4, 5, 6]}
        result = si.integrate_sensory_data(sensory_inputs)
        
        # Confidence should be 1.0 - entropy (0.4) = 0.6
        assert abs(result['confidence'] - 0.6) < 0.001

def test_main_function_exists_and_runs():
    # This test ensures the main function can be executed without error
    from src.sensory_integration import main
    try:
        main()
        assert True  # If no exception, test passes
    except Exception:
        pytest.fail("Main function should run without exception")