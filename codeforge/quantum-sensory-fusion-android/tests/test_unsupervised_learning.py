import numpy as np
import pytest
from unittest.mock import Mock, patch
from src.quantum_sensory_fusion.unsupervised_learning import SensoryClustering, quantum_enhanced_clustering, hybrid_quantum_clustering

def test_sensory_clustering_kmeans_initialization():
    clustering = SensoryClustering(method='kmeans')
    assert clustering.method == 'kmeans'
    assert clustering.is_fitted is False

def test_sensory_clustering_dbscan_initialization():
    clustering = SensoryClustering(method='dbs4can')
    assert clustering.method == 'dbscan'

def test_sensory_clustering_invalid_method():
    with pytest.raises(ValueError, match="Unsupported clustering method"):
        SensoryClustering(method='invalid_method')

def test_fit_predict_with_valid_data():
    clustering = SensoryClustering()
    X = np.array([[1, 2], [3, 4], [5, 6]])
    labels = clustering.fit_predict(X)
    assert len(labels) == X.shape[0]

def test_fit_predict_empty_data():
    clustering = SensoryClustering()
    X = np.array([])
    with pytest.raises(ValueError):
        clustering.fit_predict(X)

def test_fit_predict_kmeans_clustering():
    X = np.array([[1, 2], [2, 3], [3, 4], [10, 11], [11, 12], [12, 13]])
    clustering = SensoryClustering(method='kmeans')
    labels = clustering.fit_predict(X)
    assert len(labels) == X.shape[0]

def test_fit_predict_dbscan_clustering():
    X = np.array([[1, 2], [2, 3], [3, 4], [10, 11], [11, 12], [12, 13]])
    clustering = SensoryClustering(method='dbscan')
    labels = clustering.fit_predict(X)
    assert len(labels) == X.shape[0]

def test_transform_sensory_data_pca():
    X = np.random.rand(100, 5)
    clustering = SensoryClustering()
    result = clustering.transform_sensory_data(X, method='pca', n_components=2)
    assert result.shape[0] == X.shape[0]
    assert result.shape[1] == 2

def test_transform_sensory_data_tsne():
    X = np.random.rand(50, 10)
    clustering = SensoryClustering()
    result = clustering.transform_sensory_data(X, method='tsne', n_components=2)
    assert result.shape[0] == X.shape[0]
    assert result.shape[1] == 2

def test_transform_sensory_data_standard():
    X = np.random.rand(20, 5)
    result = SensoryClustering().transform_sensory_data(X, method='standard')
    assert result.shape == X.shape

def test_transform_sensory_data_empty():
    clustering = SensoryClustering()
    X = np.array([])
    with pytest.raises(ValueError):
        clustering.transform_sensory_data(X)

def test_quantum_enhanced_clustering():
    data = np.array([[1, 2], [2, 3], [3, 4], [10, 11], [11, 12], [12, 13]])
    labels, centers = quantum_enhanced_clustering(data, n_clusters=3)
    assert len(labels) == data.shape[0]
    assert centers is not None

def test_hybrid_quantum_clustering_kmeans():
    data = np.array([[1, 2], [2, 3], [3, 4], [10, 11], [11, 12], [12, 13]])
    labels = hybrid_quantum_clustering(data, method='kmeans')
    assert len(labels) == data.shape[0]

def test_hybrid_quantum_clustering_dbscan():
    data = np.array([[1, 2], [2, 3], [3, 4], [10, 11], [11, 12], [12, 13]])
    labels = hybrid_quantum_clustering(data, method='dbscan')
    assert len(labels) == data.shape[0]

def test_hybrid_clustering_invalid_method():
    data = np.array([[1, 2], [2, 3]])
    with pytest.raises(Exception):
        hybrid_quantum_clustering(data, method='invalid')

def test_clustering_with_various_data_shapes():
    # Test with single sample
    data_single = np.array([[1, 2]])
    clustering = SensoryClustering()
    labels = clustering.fit_predict(data_single)
    assert len(labels) == 1

def test_clustering_with_nan_values():
    data = np.array([[np.nan, 2], [3, 4]])
    clustering = SensoryClustering()
    with pytest.raises(ValueError):
        clustering.fit_predict(data)

def test_clustering_with_infinite_values():
    data = np.array([[1, np.inf], [3, 4]])
    with pytest.raises(ValueError):
        SensoryClustering().fit_predict(data)

def test_clustering_with_zero_samples():
    clustering = SensoryClustering()
    X = np.array([]).reshape(0, 2)
    with pytest.raises(ValueError):
        clustering.fit_predict(X)

def test_clustering_with_one_cluster_data():
    data = np.array([[1, 2]])
    clustering = SensoryClustering()
    labels = clustering.fit_predict(data)
    assert len(np.unique(labels)) == 1