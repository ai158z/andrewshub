import pytest
import numpy as np
from src.models.perception_model import SensoryData, QuantumState, PerceptionModel
from typing import List, Dict, Any


def test_sensory_data_creation():
    """Test basic SensoryData model creation with valid data"""
    data = SensoryData(
        timestamp=1234567890.0,
        sensor_id="sensor_1",
        data={"temperature": 25.5, "humidity": 60.0}
    )
    assert data.timestamp == 1234567890.0
    assert data.sensor_id == "sensor_1"
    assert data.data["temperature"] == 25.5


def test_sensory_data_default_factory():
    """Test that data field uses default factory correctly"""
    sensory = SensoryData(timestamp=1234567890.0, sensor_id="test")
    assert sensory.data == {}


def test_quantum_state_creation():
    """Test QuantumState model creation with valid data"""
    state = QuantumState(
        state_vector=[1+0j, 0+1j],
        qubit_count=2,
        entanglement=[[0.5, 0.5], [0.5, 0.5]]
    )
    assert state.qubit_count == 2
    assert state.entanglement is not None


def test_perception_model_process_sensory_data():
    """Test processing of sensory data returns expected structure"""
    model = PerceptionModel(
        sensory_input=SensoryData(timestamp=1234567890.0, sensor_id="test"),
        quantum_state=QuantumState(
            state_vector=[1+0j, 0+1j],
            qubit_count=2
        )
    )
    result = model.process_sensory_data()
    assert "status" in result
    assert result["status"] == "processed"


def test_perception_model_process_sensory_data_features():
    """Test that processed features are returned correctly"""
    model = PerceptionModel(
        sensory_input=SensoryData(timestamp=1234567890.0, sensor_id="test"),
        quantum_state=QuantumState(
            state_vector=[1+0j, 0+1j],
            qubit_count=2
        )
    )
    result = model.process_sensory_data()
    assert "features" in result
    assert "timestamp" in result


def test_perception_model_get_perception_state():
    """Test getting perception state returns copy of features"""
    model = PerceptionModel(
        sensory_input=SensoryData(timestamp=1234567890.0, sensor_id="test"),
        quantum_state=QuantumState(
            state_vector=[1+0j, 0+1j],
            qubit_count=2
        ),
        processed_features={"feature1": "value1", "feature2": "value2"}
    )
    state = model.get_perception_state()
    assert "feature1" in state
    assert "feature2" in state


def test_perception_model_update_quantum_state():
    """Test updating quantum state with new information"""
    model = PerceptionModel(
        sensory_input=SensoryData(timestamp=1234567890.0, sensor_id="test"),
        quantum_state=QuantumState(
            state_vector=[1+0j, 0+1j],
            qubit_count=2
        )
    )
    new_state = {"quantum_param": 1.0}
    model.update_quantum_state(new_state)
    assert "quantum_param" in model.processed_features


def test_perception_model_get_adaptation_parameters():
    """Test getting adaptation parameters returns correct state"""
    model = PerceptionModel(
        sensory_input=SensoryData(timestamp=1234567890.0, sensor_id="test"),
        quantum_state=QuantumState(
            state_vector=[1+0j, 0+1j],
            qubit_count=2
        ),
        adaptation_state={"learning_rate": 0.01, "momentum": 0.9}
    )
    params = model.get_adaptation_parameters()
    assert "learning_rate" in params
    assert "momentum" in params


def test_sensory_data_validation():
    """Test that sensory data validation works correctly"""
    # Test valid sensory data
    data = SensoryData(timestamp=1234567890.0, sensor_id="test_sensor")
    assert data.timestamp == 1234567890.0
    assert data.sensor_id == "test_sensor"


def test_quantum_state_validation():
    """Test that quantum state validation works correctly"""
    state = QuantumState(
        state_vector=[1+0j, 0+1j, 1+1j],
        qubit_count=3
    )
    assert len(state.state_vector) == 3
    assert state.qubit_count == 3


def test_perception_model_validation():
    """Test that perception model validation works correctly"""
    sensory_input = SensoryData(timestamp=1234567890.0, sensor_id="test")
    quantum_state = QuantumState(
        state_vector=[1+0j, 0+1j],
        qubit_count=2
    )
    model = PerceptionModel(
        sensory_input=sensory_input,
        quantum_state=quantum_state
    )
    assert model.sensory_input.timestamp == 1234567890.0
    assert model.quantum_state.qubit_count == 2


def test_sensory_data_empty_dict_default():
    """Test that sensory data uses empty dict as default"""
    data = SensoryData(timestamp=1234567890.0, sensor_id="test")
    assert data.data == {}


def test_quantum_state_empty_entanglement_default():
    """Test that quantum state handles empty entanglement"""
    state = QuantumState(
        state_vector=[1+0j, 0+1j],
        qubit_count=2
    )
    assert state.entanglement is None


def test_perception_model_pattern_matches_default():
    """Test that pattern matches default to empty list"""
    model = PerceptionModel(
        sensory_input=SensoryData(timestamp=1234567890.0, sensor_id="test"),
        quantum_state=QuantumState(
            state_vector=[1+0j, 0+1j],
            qubit_count=2
        )
    )
    assert model.pattern_matches == []


def test_perception_model_response_actions_default():
    """Test that response actions default to empty list"""
    model = PerceptionModel(
        sensory_input=SensoryData(timestamp=1234567890.0, sensor_id="test"),
        quantum_state=QuantumState(
            state_vector=[1+0j, 0+1j],
            qubit_count=2
        )
    )
    assert model.response_actions == []


def test_sensory_data_with_custom_data():
    """Test sensory data with custom data field"""
    data = SensoryData(
        timestamp=1234567890.0,
        sensor_id="test",
        data={"custom_field": "value"}
    )
    assert data.data["custom_field"] == "value"


def test_quantum_state_complex_validation():
    """Test quantum state with complex numbers validation"""
    state = QuantumState(
        state_vector=[1+2j, 3+4j],
        qubit_count=2,
        entanglement=None
    )
    assert state.state_vector[0] == 1+2j
    assert state.state_vector[1] == 3+4j


def test_perception_model_with_custom_features():
    """Test perception model with custom features"""
    model = PerceptionModel(
        sensory_input=SensoryData(timestamp=1234567890.0, sensor_id="test"),
        quantum_state=QuantumState(
            state_vector=[1+0j, 0+1j],
            qubit_count=2,
            entanglement=[[0.5, 0.5], [0.5, 0.5]]
        ),
        processed_features={"feature1": "test", "feature2": "data"}
    )
    assert "feature1" in model.processed_features


def test_perception_model_entanglement_matrix():
    """Test quantum state with entanglement matrix"""
    state = QuantumState(
        state_vector=[1+0j, 0+1j],
        qubit_count=2,
        entanglement=[[1.0, 0.0], [0.0, 1.0]]
    )
    assert state.entanglement is not None
    assert len(state.entanglement) == 2


def test_perception_model_sensory_pipeline():
    """Test the complete sensory processing pipeline"""
    sensory_data = SensoryData(
        timestamp=1234567890.0,
        sensor_id="test_sensor"
    )
    quantum_state = QuantumState(
        state_vector=[1+0j, 0+1j],
        qubit_count=2
    )
    model = PerceptionModel(
        sensory_input=sensory_data,
        quantum_state=quantum_state
    )
    result = model.process_sensory_data()
    assert result["status"] == "processed"
    assert result["timestamp"] == 1234567890.0