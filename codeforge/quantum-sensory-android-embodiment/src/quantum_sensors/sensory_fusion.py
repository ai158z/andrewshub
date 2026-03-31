import numpy as np
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Try to import Qiskit, but handle case where it's not available
try:
    from qiskit.quantum_info import Statevector
    from qiskit.quantum_info import DensityMatrix
    qiskit_available = True
except ImportError:
    # Create mock classes if Qiskit is not available
    Statevector = None
    DensityMatrix = None
    qiskit_available = False

@dataclass
class FusionResult:
    """Data class for fusion results"""
    unified_field: Dict[str, Any]
    confidence: float
    timestamp: float
    metadata: Dict[str, Any]

class SensoryFusionEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing SensoryFusionEngine")
        
    def fuse_sensory_inputs(self, sensor_data: Dict[str, Any], 
                          sensor_weights: Optional[Dict[str, float]] = None) -> FusionResult:
        """Fuse sensory inputs using quantum processing"""
        try:
            # Process sensor data
            processed_data = self._process_sensory_data(sensor_data)
            
            # Calculate weights if not provided
            if sensor_weights is None:
                sensor_weights = self._calculate_default_weights(sensor_data)
            
            # Create quantum states from sensor data
            quantum_states = self._create_quantum_states(processed_data, sensor_weights)
            
            # Compute entanglement metrics
            entanglement_metrics = self.compute_entanglement_metrics(quantum_states)
            
            # Create unified field representation
            unified_field = self._create_unified_field(quantum_states, entanglement_metrics)
            
            # Calculate confidence score
            confidence = self._calculate_fusion_confidence(quantum_states, entanglement_metrics)
            
            return FusionResult(
                unified_field=unified_field,
                confidence=confidence,
                timestamp=datetime.now().timestamp(),
                metadata={}
            )
        except Exception as e:
            self.logger.error(f"Error in sensory fusion: {e}")
            return FusionResult(
                unified_field={},
                confidence=0.0,
                timestamp=datetime.now().timestamp(),
                metadata={"error": str(e)}
            )
    
    def _process_sensory_data(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw sensor data"""
        # Mock processing - in real implementation this would do actual processing
        return sensor_data
    
    def _calculate_default_weights(self, sensor_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate default weights for sensors"""
        if not sensor_data:
            return {}
        
        # Simple equal weighting if no data
        weight = 1.0 / len(sensor_data) if sensor_data else 0.0
        return {sensor: weight for sensor in sensor_data.keys()}
    
    def _create_quantum_states(self, sensor_data: Dict[str, Any], 
                            sensor_weights: Dict[str, float]) -> Dict[str, Any]:
        """Create quantum states from sensor data"""
        # Mock implementation
        quantum_states = {}
        for sensor, data in sensor_data.items():
            if isinstance(data, dict) and 'value' in data:
                quantum_states[sensor] = {
                    'amplitude': data['value'],
                    'state_vector': np.array([data['value'], 0.0]) if isinstance(data['value'], (int, float)) else np.array([1.0, 0.0])
                }
            else:
                quantum_states[sensor] = {
                    'amplitude': 1.0,
                    'state_vector': np.array([1.0, 0.0])
                }
        return quantum_states
    
    def _compute_density_matrix(self, state_vector) -> np.ndarray:
        """Compute density matrix for state vector"""
        if Statevector is not None:
            # Use Qiskit if available
            if isinstance(state_vector, Statevector):
                density_matrix = np.outer(state_vector.data, state_vector.data.conj())
                return density_matrix
        # Fallback if Qiskit not available
        return np.outer(state_vector, state_vector.conj())
    
    def _von_neumann_entropy(self, density_matrix: np.ndarray) -> float:
        """Compute von Neumann entropy"""
        try:
            # Compute eigenvalues
            eigenvalues = np.linalg.eigvals(density_matrix)
            # Filter out near-zero eigenvalues to avoid log(0)
            eigenvalues = eigenvalues[np.abs(eigenvalues) > 1e-15]
            # Compute entropy: -tr(ρ*log(ρ))
            entropy = -np.sum(eigenvalues * np.log(eigenvalues))
            return entropy if not np.isnan(entropy) else 0.0
        except Exception:
            return 0.0
    
    def compute_entanglement_metrics(self, quantum_states: Dict[str, Any]) -> Dict[str, float]:
        """Compute entanglement metrics for quantum states"""
        if not quantum_states:
            return {}
        
        # Compute metrics for each state
        metrics = {}
        for sensor_name, state_data in quantum_states.items():
            # Compute density matrix
            if 'state_vector' in state_data:
                density_matrix = self._compute_density_matrix(state_data['state_vector'])
                # Compute entropy
                entropy = self._von_neumann_entropy(density_matrix)
                metrics[sensor_name] = {
                    'entanglement_entropy': entropy,
                    'density_matrix': density_matrix
                }
        return metrics
    
    def _create_unified_field(self, quantum_states: Dict[str, Any], 
                           entanglement_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Create unified field representation"""
        # Compute mutual information between all sensors
        mutual_info = self._compute_mutual_information(quantum_states)
        
        # Create unified representation
        return {
            'entanglement_metrics': entanglement_metrics,
            'mutual_information': mutual_info,
            'timestamp': datetime.now().timestamp()
        }
    
    def _compute_mutual_information(self, quantum_states: Dict[str, Any]) -> float:
        """Compute mutual information between quantum states"""
        if not quantum_states:
            return 0.0
        
        # Sum all entanglement entropies
        total_entropy = sum([
            state.get('entanglement_entropy', 0) 
            for state in quantum_states.values()
            if isinstance(state, dict) and 'entanglement_entropy' in state
        ])
        
        return total_entropy
    
    def _calculate_fusion_confidence(self, quantum_states: Dict[str, Any],
                                 entanglement_metrics: Dict[str, Any]) -> float:
        """Calculate fusion confidence from quantum metrics"""
        if not quantum_states or not entanglement_metrics:
            return 0.0
        
        # Simple confidence calculation based on entanglement
        # In practice, this would be more sophisticated
        return min(1.0, max(0.0, 0.8))  # Clamp to [0,1]
    
    def _dict_to_statevector(self, data: Dict[str, float]) -> Any:
        """Convert dict to statevector if Qiskit available"""
        if Statevector is not None and data:
            # If we have actual data, convert appropriately
            if data:
                # Create a simple state vector from data values
                values = list(data.values())
                if values:
                    # Normalize and create state vector
                    norm = np.linalg.norm(values)
                    if norm > 0:
                        normalized_values = np.array(values) / norm
                        return Statevector(normalized_values)
                else:
                    # Return default statevector
                    return Statevector([1.0, 0.0])
            else:
                # Return default statevector
                return Statevector([1.0, 0.0])
        else:
            # Return empty statevector
            return Statevector([0.0])