import numpy as np
import pytest
from unittest.mock import Mock, patch, MagicMock
import networkx as nx

from codonic_layer.sensory_integration import SensoryIntegration


class TestSensoryIntegration:
    
    @patch('codonic_layer.sensory_integration.MPNN')
    @patch('codonic_layer.sensory_integration.QuantumStates')
    @patch('codonic_layer.sensory_integration.InterferenceTracker')
    def test_process_sensory_input_validates_input_type(self, mock_interference_tracker, mock_quantum_states, mock_mpnn):
        """Test that process_sensory_input validates input is dictionary"""
        si = SensoryIntegration()
        si.mpnn = mock_mpnn
        si.quantum_states = mock_quantum_states
        si.interference_tracker = mock_interference_tracker
        
        with pytest.raises(TypeError):
            si.process_sensory_input("invalid_input")
    
    def test_process_sensory_input_validates_required_modalities(self):
        """Test that process_sensory_input checks for required modalities"""
        si = SensoryIntegration()
        sensory_data = {
            'visual': [1, 2, 3],
            'auditory': [4, 5, 6],
            # Missing other modalities
        }
        
        with pytest.raises(ValueError, match="Missing required sensory modalities"):
            si.process_sensory_input(sensory_data)
    
    def test_process_sensory_input_success(self):
        """Test successful processing of sensory input"""
        si = SensoryIntegration()
        sensory_data = {
            'visual': [1, 2, 3],
            'auditory': [4, 5, 6],
            'tactile': [7, 8, 9],
            'olfactory': [10, 11, 12],
            'gustatory': [13, 14, 15]
        }
        
        # Should not raise an error
        result = si.process_sensory_input(sensory_data)
        assert 'graph_data' in result
        assert 'embeddings' in result
        assert 'quantum_state' in result
    
    def test_integrate_modality_validates_modality(self):
        """Test that integrate_modality validates modality type"""
        si = SensoryIntegration()
        
        with pytest.raises(ValueError, match="Unsupported modality"):
            si.integrate_modality('invalid_modality', [1, 2, 3])
    
    def test_integrate_modality_success(self):
        """Test successful modality integration"""
        si = SensoryIntegration()
        # Mock the MPNN to avoid actual processing
        si.mpnn = Mock()
        si.mpnn.forward_pass.return_value = np.array([1.0, 2.0, 3.0])
        
        result, confidence = si.integrate_modality('visual', [1, 2, 3])
        assert isinstance(result, np.ndarray)
        assert isinstance(confidence, float)
    
    def test_get_sensory_state_returns_state(self):
        """Test that get_sensory_state returns proper structure"""
        si = SensoryIntegration()
        si.quantum_states.get_state = Mock(return_value=np.array([1, 2, 3]))
        si.interference_tracker.get_pattern_analysis = Mock(return_value={'test': 'data'})
        
        result = si.get_sensory_state()
        assert 'quantum_state' in result
        assert 'interference_data' in result
        assert 'sensory_graph' in result
    
    def test_map_to_action_processes_state_data(self):
        """Test that map_to_action processes state data"""
        si = SensoryIntegration()
        si.mpnn.process_graph = Mock(return_value=np.array([1, 2, 3]))
        si.quantum_states.measure = Mock(return_value=np.array([0.5, 0.3, 0.2]))
        
        state_data = {'test': 'data'}
        result = si.map_to_action(state_data)
        assert 'action_vector' in result
        assert 'quantum_measurement' in result
        assert 'confidence' in result
    
    def test_create_sensory_graph_builds_graph(self):
        """Test that _create_sensory_graph builds proper graph structure"""
        si = SensoryIntegration()
        sensory_data = {
            'visual': [1, 2, 3],
            'auditory': [4, 5, 6]
        }
        
        graph = si._create_sensory_graph(sensory_data)
        assert isinstance(graph, nx.Graph)
        assert len(graph.nodes()) > 0
    
    def test_sensory_integration_initializes_components(self):
        """Test that SensoryIntegration initializes all components"""
        si = SensoryIntegration()
        assert si.quantum_states is not None
        assert si.mpnn is not None
        assert si.interference_tracker is not None
        assert isinstance(si.modality_weights, dict)
        assert len(si.modality_weights) == 5
    
    def test_integration_threshold_configuration(self):
        """Test that integration threshold is properly configured"""
        si = SensoryIntegration()
        assert si.integration_threshold == 0.7
    
    def test_modality_weights_assignment(self):
        """Test that modality weights are properly assigned"""
        si = SensoryIntegration()
        expected_weights = {
            'visual': 1.0,
            'auditory': 0.8,
            'tactile': 0.6,
            'olfactory': 0.4,
            'gustatory': 0.4
        }
        assert si.modality_weights == expected_weights
    
    def test_process_sensory_input_creates_graph(self):
        """Test that process_sensory_input creates proper graph"""
        si = SensoryIntegration()
        sensory_data = {
            'visual': [1, 2, 3],
            'auditory': [4, 5, 6],
            'tactile': [7, 8, 9],
            'olfactory': [10, 11, 12],
            'gustatory': [13, 14, 15]
        }
        
        result = si.process_sensory_input(sensory_data)
        assert 'graph_data' in result
        assert isinstance(result['graph_data'], nx.Graph)
    
    def test_apply_sensory_weights_applies_weights(self):
        """Test that _apply_sensory_weights applies correct weights"""
        si = SensoryIntegration()
        data = np.array([1.0, 2.0, 3.0])
        weighted_data = si._apply_sensory_weights(data, 'visual')
        assert not np.array_equal(data, weighted_data)
        # Check that data has been modified by weights
        assert np.allclose(weighted_data, data * si.modality_weights['visual'])
    
    def test_calculate_action_confidence_computes_confidence(self):
        """Test that _calculate_action_confidence computes confidence"""
        si = SensoryIntegration()
        action_vector = np.array([1.0, 2.0, 3.0])
        measurement = np.array([0.5, 0.3, 0.2])
        
        confidence = si._calculate_action_confidence(action_vector, measurement)
        assert isinstance(confidence, float)
        assert confidence >= 0.0
    
    def test_integrate_modality_returns_processed_data(self):
        """Test that integrate_modality returns processed data and confidence"""
        si = SensoryIntegration()
        si.mpnn.forward_pass = Mock(return_value=np.array([1.0, 2.0, 3.0]))
        
        processed, confidence = si.integrate_modality('visual', [1, 2, 3])
        assert isinstance(processed, np.ndarray)
        assert isinstance(confidence, float)
    
    def test_sensory_graph_creation(self):
        """Test that sensory graph is created with correct structure"""
        si = SensoryIntegration()
        sensory_data = {
            'visual': [1, 2, 3],
            'auditory': [4, 5, 6]
        }
        
        graph = si._create_sensory_graph(sensory_data)
        assert 'visual' in graph.nodes()
        assert 'auditory' in graph.nodes()
        assert 'spatial' in graph.nodes()
        assert 'temporal' in graph.nodes()
    
    def test_process_sensory_input_returns_results(self):
        """Test that process_sensory_input returns expected results"""
        si = SensoryIntegration()
        si.mpnn.process_graph = Mock(return_value=np.array([1, 2, 3]))
        si.quantum_states.initialize_superposition = Mock(return_value=np.array([1, 2, 3]))
        
        sensory_data = {
            'visual': [1, 2, 3],
            'auditory': [4, 5, 6],
            'tactile': [7, 8, 9],
            'olfactory': [10, 11, 12],
            'gustatory': [13, 14, 15]
        }
        
        result = si.process_sensory_input(sensory_data)
        assert 'graph_data' in result
        assert 'embeddings' in result
        assert 'quantum_state' in result
    
    def test_sensory_integration_modality_weights(self):
        """Test that SensoryIntegration has correct modality weights"""
        si = SensoryIntegration()
        expected_weights = {
            'visual': 1.0,
            'auditory': 0.8,
            'tactile': 0.6,
            'olfactory': 0.4,
            'gustatory': 0.4
        }
        assert si.modality_weights == expected_weights
    
    def test_sensory_integration_graph_structure(self):
        """Test that sensory integration creates proper graph structure"""
        si = SensoryIntegration()
        sensory_data = {
            'visual': [1, 2, 3],
            'auditory': [4, 5, 6],
            'tactile': [7, 8, 9],
            'olfactory': [10, 11, 12],
            'gustatory': [13, 14, 15]
        }
        
        graph = si._create_sensory_graph(sensory_data)
        assert isinstance(graph, nx.Graph)
        assert len(graph.nodes()) > 0
    
    def test_sensory_integration_action_mapping(self):
        """Test that action mapping works correctly"""
        si = SensoryIntegration()
        si.mpnn.process_graph = Mock(return_value=np.array([1, 2, 3]))
        si.quantum_states.measure = Mock(return_value=np.array([0.5, 0.3, 0.2]))
        
        state_data = {'test': 'data'}
        result = si.map_to_action(state_data)
        assert 'action_vector' in result
        assert 'quantum_measurement' in result
    
    def test_sensory_integration_error_handling(self):
        """Test that SensoryIntegration handles errors properly"""
        si = SensoryIntegration()
        
        # Test with missing modalities
        with pytest.raises(ValueError):
            sensory_data = {'visual': [1, 2, 3]}  # Missing other modalities
            si.process_sensory_input(sensory_data)
    
    def test_sensory_integration_quantum_states(self):
        """Test that quantum states are processed correctly"""
        si = SensoryIntegration()
        si.quantum_states.get_state = Mock(return_value=np.array([1, 2, 3]))
        si.interference_tracker.get_pattern_analysis = Mock(return_value={'test': 'data'})
        
        result = si.get_sensory_state()
        assert 'quantum_state' in result
        assert 'interference_data' in result
    
    def test_sensory_integration_attention_weights(self):
        """Test that attention weights are applied correctly"""
        si = SensoryIntegration()
        assert len(si.attention_weights) == 5
        # All weights should be 1.0 initially
        assert all(w == 1.0 for w in si.attention_weights)
    
    def test_sensory_integration_graph_creation_and_processing(self):
        """Test that graph creation and processing works"""
        si = SensoryIntegration()
        sensory_data = {
            'visual': [1, 2, 3],
            'auditory': [4, 5, 6],
            'tactile': [7, 8, 9],
            'olfactory': [10, 11, 12],
            'gustatory': [13, 14, 15]
        }
        
        # Create graph
        graph = si._create_sensory_graph(sensory_data)
        assert isinstance(graph, nx.Graph)
        assert len(graph.nodes()) >= 5
        
        # Process through MPNN (mocked)
        si.mpnn.process_graph = Mock(return_value=sensory_data)
        result = si.process_sensory_input(sensory_data)
        assert 'graph_data' in result
        assert 'embeddings' in result
        assert 'quantum_state' in result
    
    def test_sensory_integration_component_initialization(self):
        """Test that all components initialize correctly"""
        si = SensoryIntegration()
        assert si.quantum_states is not None
        assert si.mpnn is not None
        assert si.interference_tracker is not None
        assert si.sensory_graph is not None
        assert isinstance(si.state_cache, dict)
        assert si.modality_weights is not None
        assert isinstance(si.attention_weights, np.ndarray)