import numpy as np
import networkx as nx
from typing import Dict, Any, List, Union
import logging

class SensoryIntegration:
    """Integrates multi-modal sensory data using Message Passing Neural Networks (MPNN) for neural processing."""
    
    def __init__(self):
        self.log_prefix = "SENSORY_INTEGRATION"
        self.logger = logging.getLogger(self.log_prefix)
        self.quantum_states = QuantumStates()
        self.mpnn = MPNN()
        self.interference_tracker = InterferenceTracker()
        self.sensory_graph = nx.Graph()
        self.state_cache = {}
        self.modality_weights = {
            'visual': 1.0,
            'auditory': 0.8,
            'tactile': 0.6,
            'olfactory': 0.4,
            'gustatory': 0.4
        }
        self.integration_threshold = 0.7
        self.attention_weights = [1.0] * 5
        self.integration_threshold = 0.7
        self.modality_weights = {
            'visual': 1.0,
            'auditory': 0.8,
            'tactile': 0.6,
            'olfactory': 0.4,
            'gutatory': 0.4
        }
        self.attention_weights = np.array([1.0] * 5)  # Equal weights for 5 modalities

    def process_sensory_input(self, sensory_data: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(sensory_data, dict):
            raise TypeError("sensory_data must be a dictionary")
        
        # Validate and structure input data
        if not all(modality in sensory_data for modality in self.modality_weights.keys()):
            missing = set(self.modality_weights.keys()) - set(sensory_data.keys())
            raise ValueError(f"Missing required sensory modalities: {missing}")
        
        # Create a graph representation of sensory data
        graph_data = self._create_sensory_graph(sensory_data)
        embeddings = self.mpnn.process_graph(graph_data)
        quantum_encoded = self.quantum_states.initialize_superposition(embeddings)
        
        return {
            'graph_data': graph,
            'embeddings': embeddings,
            'quantum_state': quantum_encoded
        }

    def integrate_modality(self, modality: str, data: Union[List, np.ndarray]]) -> Tuple[np.ndarray, float]:
        if modality not in self.modality_weights:
            raise ValueError(f"Unsupported modality: {modality}")
        
        # Weight the input based on modality importance
        weight = self.modality_weights.get(modality, 0.5)
        weighted_data = np.array(data) * weight
        
        # Process through MPNN
        processed = self.mpnn.forward_pass(weighted_data)
        confidence = float(np.var(processed) * weight)
        
        return (processed, confidence)

    def get_sensory_state(self) -> Dict[str, Any]:
        # Get current quantum state
        state = self.quantum_states.get_state()
        
        # Get interference patterns
        interference = self.interference_tracker.get_pattern_analysis()
        
        return {
            'quantum_state': state,
            'interference_data': interference,
            'sensory_graph': self.sensory_graph
        }

    def map_to_action(self, state_data: Dict[str, Any]) -> Dict[str, Any]:
        # Process state through MPNN for action mapping.
        action_space = self.mpnn.process_graph(state_data)
        measured_state = self.quantum_states.measure()
        action_response = {
            'action_vector': action_space,
            'quantum_measurement': measured_state
        }
        return action_response

    def _create_sensory_graph(self, sensory_data: Dict[str, Any]]) -> nx.Graph:
        # Add modality nodes
        for modality, data in sensory_data.items():
            graph.add_node(modality, features=data)
            
            # Add edges based on modality relationships
            if modality == 'visual':
                graph.add_edge('visual', 'spatial', weight=1.0)
            elif modality == 'auditory':
                graph.add_edge('auditory', 'temporal', weight=0.8)
            elif modality == 'tactile':
                graph.add_edge('tactile', 'pressure', weight=0.6)
        
        return graph

    def _calculate_action_confidence(self, action_vector: np.ndarray, measurement: Any) -> float:
        # Simple confidence based on variance and measurement alignment
        variance = np.var(action_vector) if len(action_vector.shape) > 1 else 0
        if len(action_vector.shape) > 1:
            fidelity = np.dot(action_vector.flatten(), measurement.flatten()) if hasattr(measurement, 'flatten') and hasattr(measurement, 'flatten') else 0
        else:
            fidelity = action_vector @ measurement if hasattr(measurement, 'flatten') and measurement.shape == action_vector.shape else 0
        
        return float(np.abs(fidelity) * (1.0 - variance))

    def _apply_sensory_weights(self, data: np.ndarray, modality: str) -> np.ndarray:
        # Apply modality-specific weights to input data.
        weight = self.modality_weights.get(modality, 0.5)
        return data * weight

    def get_sensory_state(self) -> Dict[str, Any]:
        # Get current quantum state
        state = self.quantum_states.get_state()
        # Get interference patterns
        interference = self.interference_tracker.get_pattern_analysis()
        return {
            'quantum_state': state,
            'interference_data': interference,
            'sensory_graph': self.sensory_graph
        }

    def map_to_action(self, state_data: Dict[str, Any]) -> Dict[str, Any]:
        # Process state through MPNN for action mapping.
        action_space = self.mpnn.process_graph(state_data)
        measured_state = self.quantum_states.measure()
        action_response = {
            'action_vector': action_space,
            'quantum_measurement': measured_state
        }
        return action_response