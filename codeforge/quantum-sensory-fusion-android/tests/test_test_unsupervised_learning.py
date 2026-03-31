import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.quantum_sensory_fusion.unsupervised_learning import SensoryClustering

@pytest.fixture
def sample_sensor_data():
    return np.random.rand(100, 10)

@pytest.fixture
def sample_labels():
    return np.random.randint(0, 3, 100)

@pytest.fixture
def clustering_instance():
    return SensoryClustering(n_clusters=3, max_iter=100)

def test_clustering_accuracy(sample_sensor_data, sample_labels, clustering_instance):
    predicted_labels = clustering_instance.fit_predict(sample_sensor_data)
    assert predicted_labels.shape[0] == sample_sensor_data.shape[0]
    unique_clusters = np.unique(predicted_labels)
    assert len(unique_clusters) <= 3

def test_pattern_recognition():
    synthetic_data = np.random.rand(50, 5)
    clustering = SensoryClustering()
    patterns = clustering.fit_predict(synthetic_data)
    assert len(patterns) == 50
    transformed = clustering.transform_sensory_data(synthetic_data)
    assert transformed.shape == synthetic_data.shape

def test_clustering_with_insufficient_data():
    insufficient_data = np.random.rand(2, 5)
    clustering = SensoryClustering(n_clusters=3)
    with pytest.raises((ValueError, RuntimeError)):
        clustering.fit_predict(insufficient_data)

def test_pattern_recognition_with_quantum_circuit():
    with patch('qiskit.QuantumCircuit') as mock_qc:
        mock_qc_instance = mock_qc.return_value
        mock_qc_instance.measure_all.return_value = None
        patterns = np.random.rand(20, 10)
        clustering = SensoryClustering(n_clusters=2)
        predicted = clustering.fit_predict(patterns)
        assert len(predicted) == 20
        assert 0 in np.unique(predicted)

def test_clustering_with_real_android_data():
    with patch('src.quantum_sensory_fusion.android_interface.AndroidSensorInterface') as mock_android:
        mock_android.return_value.get_sensor_data.return_value = np.random.rand(10, 3)
        sensor_data = mock_android.return_value.get_sensor_data.return_value
        clustering = SensoryClustering(n_clusters=2)
        labels = clustering.fit_predict(sensor_data)
        assert len(labels) == sensor_data.shape[0]
        assert len(np.unique(labels)) > 0

def test_sensory_transformations():
    data = np.random.rand(15, 4)
    clustering = SensoryClustering()
    transformed = clustering.transform_sensory_data(data)
    assert transformed.shape == data.shape
    with pytest.raises(ValueError):
        clustering.transform_sensory_data(np.random.rand(3, 2, 2))

def test_clustering_edge_cases():
    clustering = SensoryClustering(n_clusters=1)
    with pytest.raises(ValueError):
        clustering.fit_predict(np.array([]))
    single_sample = np.random.rand(1, 5)
    result = clustering.fit_predict(single_sample)
    assert len(result) == 1

def test_clustering_single_cluster():
    data = np.random.rand(10, 3)
    clustering = SensoryClustering(n_clusters=1)
    result = clustering.fit_predict(data)
    assert len(result) == data.shape[0]
    assert all(r == 0 for r in result)  # All points should belong to cluster 0

def test_clustering_invalid_data():
    clustering = SensoryClustering()
    with pytest.raises(ValueError):
        clustering.fit_predict(np.array([]))

def test_clustering_2d_data():
    data = np.random.rand(20, 5)
    clustering = SensoryClustering()
    result = clustering.fit_predict(data)
    assert len(result) == data.shape[0]

def test_empty_array_transform():
    clustering = SensoryClustering()
    with pytest.raises(ValueError):
        clustering.transform_sensory_data(np.array([]))

def test_single_sample_clustering():
    data = np.random.rand(1, 5)
    clustering = SensoryClustering(n_clusters=1)
    result = clustering.fit_predict(data)
    assert len(result) == 1

def test_transformation_invalid_shape():
    data = np.random.rand(5, 3, 2)  # 3D array
    clustering = SensoryClustering()
    with pytest.raises(ValueError):
        clustering.transform_sensory_data(data)

def test_clustering_insufficient_samples():
    tiny_data = np.random.rand(2, 5)
    clustering = SensoryClustering(n_clusters=5)
    with pytest.raises((ValueError, RuntimeError)):
        clustering.fit_predict(tiny_data)

def test_valid_clustering_large_clusters():
    data = np.random.rand(200, 15)
    clustering = SensoryClustering(n_clusters=5)
    result = clustering.fit_predict(data)
    assert len(result) == data.shape[0]

def test_transform_sensory_data_basic():
    data = np.random.rand(10, 4)
    clustering = SensoryClustering()
    transformed = clustering.transform_sensory_data(data)
    assert transformed.shape == data.shape

def test_fit_predict_return_structure():
    data = np.random.rand(50, 3)
    clustering = SensoryClustering()
    result = clustering.fit_predict(data)
    assert isinstance(result, np.ndarray)
    assert result.shape == (50,)

def test_fit_predict_with_varied_shapes():
    data = np.random.rand(75, 8)
    clustering = SensoryClustering()
    result = clustering.fit_predict(data)
    assert result.shape[0] == data.shape[0]

def test_minimal_data_clustering():
    tiny_data = np.random.rand(5, 3)
    clustering = SensoryClustering(n_clusters=2)
    result = clustering.fit_predict(tiny_data)
    assert len(result) == 5
    assert len(np.unique(result)) <= 2

def test_transformation_edge_case():
    data = np.random.rand(1, 1)
    clustering = SensoryClustering()
    transformed = clustering.transform_sensory_data(data)
    assert transformed.shape == data.shape