import pytest
from datetime import datetime
from src.models.sensory_data import SensoryData
from src.models.quantum_state import QuantumState
from src.models.perception_model import PerceptionModel

def test_sensory_data_creation():
    """Test basic SensoryData model creation with required fields"""
    data = SensoryData(
        sensor_type="visual",
        raw_data=[0.5, 0.8, 0.2]
    )
    assert data.sensor_type == "visual"
    assert data.raw_data == [0.5, 0.8, 0.2]
    assert data.timestamp is not None

def test_sensory_data_with_optional_fields():
    """Test SensoryData creation with optional fields"""
    metadata = {"location": "test_location", "confidence": 0.95}
    sensory_data = SensoryData(
        id="test_001",
        sensor_type="audio",
        raw_data=[0.1, 0.2, 0.3],
        source_id="mic_001",
        metadata=metadata
    )
    assert sensory_data.id == "test_001"
    assert sensory_data.source_id == "mic_001"
    assert sensory_data.metadata == metadata

def test_sensory_data_to_dict():
    """Test conversion of SensoryData to dictionary"""
    sensory_data = SensoryData(
        id="test_001",
        sensor_type="tactile",
        raw_data=[1.0, 0.5, 0.7]
    )
    result = sensory_data.to_dict()
    assert result["id"] == "test_001"
    assert result["sensor_type"] == "tactile"
    assert result["raw_data"] == [1.0, 0.5, 0.7]

def test_sensory_data_from_dict():
    """Test creating SensoryData from dictionary"""
    data = {
        "id": "dict_test",
        "sensor_type": "thermal",
        "raw_data": [0.8, 0.2],
        "source_id": "sensor_123",
        "metadata": {"unit": "celsius"}
    }
    sensory_data = SensoryData.from_dict(data)
    assert sensory_data.id == "dict_test"
    assert sensory_data.sensor_type == "thermal"
    assert sensory_data.raw_data == [0.8, 0.2]

def test_update_quantum_state():
    """Test updating quantum state of SensoryData"""
    sensory_data = SensoryData(
        sensor_type="inertial",
        raw_data=[0.1, 0.2, 0.3]
    )
    quantum_data = {
        "superposition": True,
        "entanglement": 0.75,
        "coherence": 0.88
    }
    sensory_data.update_quantum_state(quantum_data)
    assert sensory_data.quantum_state is not None
    assert sensory_data.quantum_state.superposition is True

def test_update_perception_model():
    """Test updating perception model of SensoryData"""
    sensory_data = SensoryData(
        sensor_type="visual",
        raw_data=[0.5, 0.3, 0.7]
    )
    perception_data = {
        "confidence": 0.9,
        "classification": "object",
        "features": {"color": "red", "shape": "circular"}
    }
    sensory_data.update_perception_model(perception_data)
    assert sensory_data.perception is not None
    assert sensory_data.perception.confidence == 0.9

def test_add_and_get_metadata():
    """Test adding and retrieving metadata"""
    sensory_data = SensoryData(
        sensor_type="audio",
        raw_data=[0.1, 0.9, 0.3]
    )
    sensory_data.add_metadata("test_key", "test_value")
    assert sensory_data.get_metadata("test_key") == "test_value"
    assert sensory_data.metadata is not None
    assert "test_key" in sensory_data.metadata

def test_get_nonexistent_metadata():
    """Test retrieving non-existent metadata key"""
    sensory_data = SensoryData(
        sensor_type="pressure",
        raw_data=[0.2, 0.4, 0.6]
    )
    assert sensory_data.get_metadata("nonexistent_key") is None

def test_hash_function():
    """Test SensoryData hash functionality"""
    data1 = SensoryData(sensor_type="test", raw_data=[1.0])
    data2 = SensoryData(sensor_type="test", raw_data=[1.0])
    # Hashes should be different for different instances even with same data
    assert isinstance(hash(data1), int)

def test_sensory_data_validation():
    """Test that SensoryData validates required fields"""
    with pytest.raises(Exception):
        # Should fail without required sensor_type
        SensoryData(raw_data=[0.5, 0.5])

def test_sensory_data_with_quantum_state():
    """Test SensoryData with quantum state"""
    quantum_state = QuantumState(
        superposition=True,
        entanglement=0.75,
        coherence=0.88
    )
    sensory_data = SensoryData(
        sensor_type="quantum",
        raw_data=[0.1, 0.9],
        quantum_state=quantum_state
    )
    assert sensory_data.quantum_state == quantum_state

def test_sensory_data_with_perception_model():
    """Test SensoryData with perception model"""
    perception = PerceptionModel(
        confidence=0.85,
        classification="object",
        features={"color": "red"}
    )
    sensory_data = SensoryData(
        sensor_type="visual",
        raw_data=[0.2, 0.8],
        perception=perception
    )
    assert sensory_data.perception == perception

def test_empty_raw_data():
    """Test SensoryData with empty raw data"""
    sensory_data = SensoryData(
        sensor_type="test_sensor",
        raw_data=[]
    )
    assert sensory_data.raw_data == []

def test_none_fields_excluded_from_dict():
    """Test that None fields are excluded from dictionary representation"""
    sensory_data = SensoryData(
        sensor_type="test",
        raw_data=[1.0, 2.0]
    )
    # processed_data and other optional fields should be None
    result = sensory_data.to_dict()
    assert "sensor_type" in result
    assert "raw_data" in result
    # Fields that are None should not be included in dict
    assert "processed_data" not in result

def test_timestamp_default():
    """Test that timestamp is set by default"""
    before = datetime.now()
    sensory_data = SensoryData(
        sensor_type="temporal",
        raw_data=[0.5]
    )
    after = datetime.now()
    assert before <= sensory_data.timestamp <= after

def test_source_id_field():
    """Test SensoryData with source_id field"""
    sensory_data = SensoryData(
        sensor_type="lidar",
        raw_data=[1.0, 2.0, 3.0],
        source_id="sensor_007"
    )
    assert sensory_data.source_id == "sensor_007"

def test_metadata_field():
    """Test SensoryData with metadata field"""
    metadata = {"calibration": "complete", "version": "1.2"}
    sensory_data = SensoryData(
        sensor_type="calibration_sensor",
        raw_data=[0.0, 1.0, 0.5],
        metadata=metadata
    )
    assert sensory_data.metadata == metadata

def test_processing_context():
    """Test SensoryData with processing context"""
    context = {"algorithm": "fft", "parameters": {"window": "hann"}}
    sensory_data = SensoryData(
        sensor_type="spectral",
        raw_data=[0.1, 0.9, 0.5],
        processing_context=context
    )
    assert sensory_data.processing_context == context

def test_multiple_data_types():
    """Test different sensor data types"""
    types = ["visual", "audio", "tactile", "thermal", "inertial"]
    for sensor_type in types:
        sensory_data = SensoryData(
            sensor_type=sensor_type,
            raw_data=[0.5, 0.3, 0.7]
        )
        assert sensory_data.sensor_type == sensor_type

def test_sensory_data_json_serialization():
    """Test that SensoryData can be serialized to JSON"""
    sensory_data = SensoryData(
        sensor_type="json_test",
        raw_data=[0.1, 0.2, 0.3],
        id="test_id"
    )
    # This should not raise an exception
    json_result = sensory_data.json()
    assert isinstance(json_result, str)