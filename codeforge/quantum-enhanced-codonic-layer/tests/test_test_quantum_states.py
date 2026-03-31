import numpy as np
import pytest
from unittest.mock import Mock, patch

from codonic_layer.quantum_states import QuantumStates
from codonic_layer.interference_tracker import InterferenceTracker
from codonic_layer.identity_manager import IdentityManager
from codonic_layer.sensory_integration import SensoryIntegration
from codonic_layer.ros2_bridge import ROS2Bridge
from codonic_layer.mpnn import MPNN
from codonic_layer.utils import normalize_state, tensor_product, entanglement_entropy, fidelity_measure


def test_superposition_creation():
    """Test creation of superposition state with proper normalization"""
    quantum_state = QuantumStates()
    state = quantum_state.initialize_superposition()
    
    # Verify state is not None and has elements
    assert state is not None
    assert len(state) > 0
    
    # Verify normalization
    norm = np.linalg.norm(state)
    assert abs(norm - 1.0) < 1e-10
    
    # Verify probability sum
    prob_sum = np.sum(np.abs(state)**2)
    assert abs(prob_sum - 1.0) < 1e-10


def test_superposition_state_vector_properties():
    """Test quantum state vector properties after initialization"""
    quantum_state = QuantumStates()
    state = quantum_state.initialize_superposition()
    
    # Test state vector is complex
    assert isinstance(state, np.ndarray)
    assert state.dtype == complex


def test_state_measurement_collapse():
    """Test that measurement collapses quantum state to definite value"""
    quantum_state = QuantumStates()
    
    # Create superposition state
    state = quantum_state.initialize_superposition()
    
    # Test measurement produces definite state (0 or 1)
    measured_state = quantum_state.measure(state)
    assert measured_state in [0, 1]


def test_state_measurement_consistency():
    """Test that repeated measurements yield consistent results"""
    quantum_state = QuantumStates()
    state = quantum_state.initialize_superposition()
    
    # First measurement
    measured_state1 = quantum_state.measure(state)
    # Second measurement should be the same
    measured_state2 = quantum_state.measure(state)
    
    assert measured_state1 == measured_state2


def test_entanglement_correlation():
    """Test that entangled states are correlated"""
    state1 = QuantumStates()
    state2 = QuantumStates()
    
    # Entangle the states
    state1.entangle(state2)
    
    # Measure both states
    entangled_state = state1.get_state()
    correlated_state = state2.get_state()
    
    # Verify correlation by measurement consistency
    result1 = state1.measure(entangled_state)
    result2 = state2.measure(correlated_state)
    
    # States should measure to same values when entangled
    assert result1 == result2


def test_quantum_state_initialization():
    """Test proper initialization of QuantumStates class"""
    quantum_state = QuantumStates()
    assert quantum_state is not None


def test_interference_tracking():
    """Test interference tracking functionality"""
    interference_tracker = InterferenceTracker()
    assert interference_tracker is not None


def test_identity_management():
    """Test identity management functionality"""
    identity_manager = IdentityManager()
    assert identity_manager is not None


def test_sensory_integration_initialization():
    """Test sensory integration initialization"""
    sensory_integration = SensoryIntegration()
    assert sensory_integration is not None


def test_ros2_bridge_initialization():
    """Test ROS2 bridge initialization"""
    ros2_bridge = ROS2Bridge()
    assert ros2_bridge is not None


def test_mpnn_initialization():
    """Test MPNN initialization"""
    mpnn = MPNN()
    assert mpnn is not None


def test_utils_normalize_state():
    """Test state normalization utility function"""
    # Create test state vector
    test_state = np.array([1+0j, 0+0j])
    
    # Test normalization function
    normalized = normalize_state(test_state)
    assert np.isclose(np.linalg.norm(normalized), 1.0)


def test_utils_tensor_product():
    """Test tensor product utility function"""
    # Test tensor product of two simple states
    state1 = np.array([1, 0])
    state2 = np.array([0, 1])
    
    # Calculate tensor product
    result = tensor_product(state1, state2)
    assert result is not None


def test_utils_entanglement_entropy():
    """Test entanglement entropy calculation"""
    # Test with simple 2D state
    state = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    entropy = entanglement_entropy(state)
    assert isinstance(entropy, float)
    assert entropy >= 0


def test_utils_fidelity_measure():
    """Test fidelity measure utility function"""
    # Test with two identical states
    state = np.array([1, 0])
    fidelity = fidelity_measure(state, state)
    assert np.isclose(fidelity, 1.0)


def test_superposition_state_normalization():
    """Test that superposition state is properly normalized"""
    quantum_state = QuantumStates()
    state = quantum_state.initialize_superposition()
    
    # Check normalization
    assert np.isclose(np.linalg.norm(state), 1.0)
    
    # Check all probabilities sum to 1
    prob_sum = np.sum(np.abs(state)**2)
    assert np.isclose(prob_sum, 1.0)


def test_superposition_state_probability():
    """Test superposition state probability properties"""
    quantum_state = QuantumStates()
    state = quantum_state.initialize_superposition()
    
    # Verify all probabilities are between 0 and 1
    probabilities = np.abs(state)**2
    assert np.all(probabilities >= 0)
    assert np.all(probabilities <= 1)


def test_quantum_circuit_measurement():
    """Test quantum circuit measurement operations"""
    # Test measurement operations
    quantum_state = QuantumStates()
    state = quantum_state.initialize_superposition()
    
    # Test measurement collapses state
    measured_state = quantum_state.measure(state)
    assert measured_state in [0, 1]


def test_quantum_state_fidelity():
    """Test quantum state fidelity measurements"""
    state1 = np.array([1, 0])
    state2 = np.array([1, 0])
    
    # Test identical states have fidelity 1
    fidelity = fidelity_measure(state1, state2)
    assert np.isclose(fidelity, 1.0)


def test_entanglement_operation():
    """Test entanglement operations"""
    # Create entangled states
    state1 = QuantumStates()
    state2 = QuantumStates()
    
    # Entangle states
    state1.entangle(state2)
    
    # Test they remain entangled
    ent_state1 = state1.get_state()
    ent_state2 = state2.get_state()
    
    # Both should measure to same values
    assert np.array_equal(state1.measure(ent_state1), state2.measure(ent_state2))