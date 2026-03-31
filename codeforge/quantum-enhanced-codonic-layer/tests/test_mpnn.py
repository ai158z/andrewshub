import numpy as np
import networkx as nx
import pytest
from unittest.mock import Mock, patch

from codonic_layer.mpnn import MPNN

class TestMPNN:
    @pytest.fixture
    def mpnn(self):
        return MPNN(input_dim=4, hidden_dim=8, output_dim=4, num_layers=2, dropout_rate=0.0)  # No dropout for reproducible tests
    
    @pytest.fixture
    def sample_graph(self):
        graph = nx.Graph()
        graph.add_node(0, features=np.array([1, 2, 3, 4]))
        graph.add_node(1, features=np.array([2, 3, 4, 5]))
        graph.add_edge(0, 1)
        return graph
    
    @pytest.fixture
    def sample_data(self):
        return np.array([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]])
    
    def test_initialization(self):
        mpnn = MPNN()
        assert mpnn.input_dim == 64
        assert mpnn.hidden_dim == 128
        assert mpnn.output_dim == 32
        assert mpnn.num_layers == 3
        assert mpnn.dropout_rate == 0.1
        assert 'input' in mpnn.weights
        assert 'hidden' in mpnn.weights
        assert 'output' in mpnn.weights
    
    def test_forward_pass_with_empty_input(self, mpnn):
        with pytest.raises(ValueError, match="Input data cannot be empty"):
            mpnn.forward_pass(None)
    
    def test_forward_pass_with_empty_array(self, mpnn):
        with pytest.raises(ValueError, match="Input data cannot be empty"):
            mpnn.forward_pass(np.array([]))
    
    @patch('codonic_layer.mpnn.QuantumStates')
    def test_forward_pass_success(self, mock_quantum, mpnn, sample_data, sample_graph):
        mock_quantum_instance = mock_quantum.return_value
        mock_quantum_instance.process_sensory_input.return_value = sample_data
        
        result = mpnn.forward_pass(sample_data, sample_graph)
        assert isinstance(result, np.ndarray)
        assert len(result) > 0
    
    def test_message_passing_empty_graph(self, mpnn):
        features = np.array([[1, 2, 3, 4]])
        result = mpnn._message_passing(features)
        assert isinstance(result, np.ndarray)
    
    def test_generate_output_empty_embeddings(self, mpnn):
        result = mpnn._generate_output(np.array([]))
        assert len(result) == 0
    
    def test_generate_output_with_embeddings(self, mpnn):
        embeddings = np.array([[1, 2, 3, 4], [2, 3, 4, 5]])
        result = mpnn._generate_output(embeddings)
        assert isinstance(result, np.ndarray)
        assert result.shape[1] == mpnn.output_dim
    
    def test_update_weights_none_gradients(self, mpnn):
        # Should not raise any error when gradients are None or missing
        mpnn.update_weights({})
        # Weights should remain unchanged
        assert mpnn.weights['input'] is not None
        assert mpnn.weights['hidden'] is not None
        assert mpnn.weights['output'] is not None
    
    def test_update_weights_with_gradients(self, mpnn):
        initial_input_weight = np.copy(mpnn.weights['input'])
        initial_hidden_weight = np.copy(mpnn.weights['hidden'])
        initial_output_weight = np.copy(mpnn.weights['output'])
        
        gradients = {
            'input': np.random.rand(mpnn.hidden_dim, mpnn.input_dim),
            'hidden': np.random.rand(mpnn.hidden_dim, mpnn.hidden_dim),
            'output': np.random.rand(mpnn.output_dim, mpnn.hidden_dim)
        }
        
        mpnn.update_weights(gradients, learning_rate=0.01)
        
        # Check that weights have been updated
        assert not np.array_equal(mpnn.weights['input'], initial_input_weight)
        assert not np.array_equal(mpnn.weights['hidden'], initial_hidden_weight)
        assert not np.array_equal(mpnn.weights['output'], initial_output_weight)
    
    def test_process_graph(self, mpnn):
        sensory_data = np.array([[1, 2], [3, 4]])
        connections = [(0, 1)]
        
        graph = mpnn.process_graph(sensory_data, connections)
        
        assert len(graph.nodes()) == 2
        assert len(graph.edges()) == 1
        assert np.array_equal(graph.nodes[0]['features'], sensory_data[0])
        assert np.array_equal(graph.nodes[1]['features'], sensory_data[1])
    
    def test_get_embeddings_empty_graph(self, mpnn):
        result = mpnn.get_embeddings()
        assert len(result) == 0
    
    def test_get_embeddings_with_nodes(self, mpnn, sample_graph):
        mpnn.graph = sample_graph
        result = mpnn.get_embeddings()
        assert isinstance(result, np.ndarray)
        assert len(result) > 0
    
    def test_add_node(self, mpnn):
        features = np.array([1, 2, 3, 4])
        mpnn.add_node(5, features, (1.0, 2.0, 3.0))
        
        assert 5 in mpnn.graph.nodes()
        assert 'features' in mpnn.graph.nodes[5]
        assert np.array_equal(mpnn.graph.nodes[5]['features'], features)
    
    def test_add_edge_no_graph(self, mpnn):
        mpnn.add_edge(0, 1, 2.0)
        assert mpnn.graph is not None
        assert (0, 1) in mpnn.graph.edges()
        assert mpnn.graph[0][1]['weight'] == 2.0
    
    def test_compute_node_similarity_node_not_found(self, mpnn):
        similarity = mpnn.compute_node_similarity(0, 1)
        assert similarity == 0.0
    
    def test_compute_node_similarity_valid_nodes(self, mpnn, sample_graph):
        mpnn.graph = sample_graph
        mpnn.graph.nodes[0]['features'] = np.array([1, 0, 0])
        mpnn.graph.nodes[1]['features'] = np.array([0, 1, 0])
        
        similarity = mpnn.compute_node_similarity(0, 1)
        assert 0 <= similarity <= 1  # Cosine similarity should be normalized
    
    def test_compute_node_similarity_missing_features(self, mpnn, sample_graph):
        mpnn.graph = sample_graph
        # Remove features from one node
        del mpnn.graph.nodes[0]['features']
        
        similarity = mpnn.compute_node_similarity(0, 1)
        assert similarity == 0.0
    
    def test_forward_pass_with_isolated_graph(self, mpnn):
        # Test with graph that has no edges
        graph = nx.Graph()
        graph.add_node(0, features=np.array([1, 2, 3, 4]))
        graph.add_node(1, features=np.array([2, 3, 4, 5]))
        
        result = mpnn.forward_pass(np.array([[1, 2, 3, 4], [2, 3, 4, 5]]), graph)
        assert isinstance(result, np.ndarray)