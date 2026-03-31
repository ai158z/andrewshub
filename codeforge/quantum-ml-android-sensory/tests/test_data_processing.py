import pytest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
import warnings

# Suppress warnings for cleaner test output
warnings.filterwarnings("ignore")

@pytest.fixture
def sample_data():
    return np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'A': [1, 4, 7],
        'B': [2, 5, 8], 
        'C': [3, 6, 9]
    })

@pytest.fixture
def sample_time_series_df():
    return pd.DataFrame({
        'timestamp': pd.date_range('2023-01-01', periods=3, freq='1min'),
        'value1': [1.0, 2.0, 3.0],
        'value2': [10.0, 20.0, 30.0]
    })

@pytest.fixture
def sample_sensory_data():
    return {'sensor1': 1.0, 'sensor2': 2.0, 'timestamp': '2023-01-01T00:00:00'}

@patch('qml_framework.data_processing.initialize_framework')
def test_preprocess_data_standardize_array(mock_init, sample_data):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    result = processor.preprocess_data(sample_data, method='standardize')
    assert isinstance(result, np.ndarray)
    # Check if standardized (mean ~ 0, std ~ 1)
    assert np.allclose(result.mean(axis=0), 0, atol=1e-10)
    assert np.allclose(result.std(axis=0), 1, atol=1e-10)

@patch('qml_framework.data_processing.initialize_framework')
def test_preprocess_data_standardize_dataframe(mock_init, sample_df):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    result = processor.preprocess_data(sample_df, method='standardize')
    assert isinstance(result, pd.DataFrame)
    # All columns should be standardized
    for col in result.columns:
        assert np.isclose(result[col].mean(), 0, atol=1e-10)
        assert np.isclose(result[col].std(), 1, atol=1e-10)

@patch('qml_framework.data_processing.initialize_framework')
def test_preprocess_data_normalize(mock_init, sample_data):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    result = processor.preprocess_data(sample_data, method='normalize')
    assert isinstance(result, np.ndarray)
    # Check if normalized to [0,1] range
    assert np.all(result >= 0) and np.all(result <= 1)

@patch('qml_framework.data_processing.initialize_framework')
def test_preprocess_data_minmax(mock_init, sample_df):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    result = processor.preprocess_data(sample_df, method='minmax')
    assert isinstance(result, pd.DataFrame)
    # Check if scaled to [-1,1] range
    for col in result.columns:
        assert result[col].min() >= -1 and result[col].max() <= 1

@patch('qml_framework.data_processing.initialize_framework')
def test_preprocess_data_invalid_method(mock_init, sample_data):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    with pytest.raises(ValueError):
        processor.preprocess_data(sample_data, method='invalid')

@patch('qml_framework.data_processing.initialize_framework')
def test_extract_features_array(mock_init, sample_data):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    result = processor.extract_features(sample_data)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_data.shape

@patch('qml_framework.data_processing.initialize_framework')
def test_extract_features_dataframe(mock_init, sample_df):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    result = processor.extract_features(sample_df, ['A', 'B'])
    assert isinstance(result, np.ndarray)
    assert result.shape == (3, 2)

@patch('qml_framework.data_processing.initialize_framework')
def test_prepare_quantum_data(mock_init, sample_data):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    qc, data = processor.prepare_quantum_data(sample_data)
    from qiskit import QuantumCircuit
    assert isinstance(qc, QuantumCircuit)
    assert isinstance(data, np.ndarray)

@patch('qml_framework.data_processing.initialize_framework')
def test_apply_quantum_kernel(mock_init, sample_data):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    result = processor.apply_quantum_kernel(sample_data)
    assert isinstance(result, np.ndarray)
    assert result.shape == (sample_data.shape[0], sample_data.shape[0])

@patch('qml_framework.data_processing.initialize_framework')
def test_process_android_sensory_data_dict(mock_init, sample_sensory_data):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    result = processor.process_android_sensory_data(sample_sensory_data)
    assert isinstance(result, dict)
    assert 'processed' in result
    assert result['processed'] == True

@patch('qml_framework.data_processing.initialize_framework')
def test_normalize_tensor_data(mock_init, sample_data):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    result = processor.normalize_tensor_data(sample_data)
    assert isinstance(result, np.ndarray)
    # Check L2 normalization
    assert np.isclose(np.linalg.norm(result), 1.0)

@patch('qml_framework.data_processing.initialize_framework')
def test_filter_outliers_array(mock_init, sample_data):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    # Create data with outlier
    data_with_outlier = np.vstack([sample_data, [100, 100, 100]])
    result = processor.filter_outliers(data_with_outlier, threshold=2.0)
    assert isinstance(result, np.ndarray)
    # Outlier should be filtered out
    assert result.shape[0] < data_with_outlier.shape[0]

@patch('qml_framework.data_processing.initialize_framework')
def test_filter_outliers_dataframe(mock_init, sample_df):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    # Add outlier to dataframe
    df_with_outlier = sample_df.copy()
    df_with_outlier.loc[len(df_with_outlier)] = [100, 100, 100]
    result = processor.filter_outliers(df_with_outlier, threshold=2.0)
    assert isinstance(result, pd.DataFrame)
    # Should have filtered out the outlier row
    assert len(result) < len(df_with_outlier)

@patch('qml_framework.data_processing.initialize_framework')
def test_aggregate_time_series(mock_init, sample_time_series_df):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    result = processor.aggregate_time_series(
        sample_time_series_df, 
        'timestamp', 
        ['value1', 'value2'], 
        '1min'
    )
    assert isinstance(result, pd.DataFrame)
    assert 'timestamp' in result.columns

@patch('qml_framework.data_processing.initialize_framework')
def test_dimensionality_reduction_array(mock_init, sample_data):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    result = processor.dimensionality_reduction(sample_data, n_components=2)
    assert isinstance(result, np.ndarray)
    assert result.shape[1] == 2

@patch('qml_framework.data_processing.initialize_framework')
def test_prepare_training_data(mock_init, sample_data):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    labels = np.array([0, 1, 2])
    X, y = processor.prepare_training_data(sample_data, labels)
    assert X.shape[0] == len(y)

@patch('qml_framework.data_processing.initialize_framework')
def test_prepare_training_data_mismatch(mock_init, sample_data):
    from qml_framework.data_processing import DataProcessor
    processor = DataProcessor()
    labels = np.array([0, 1])  # Mismatched length
    with pytest.raises(ValueError):
        processor.prepare_training_data(sample_data, labels)

@patch('qml_framework.data_processing.initialize_framework')
def test_module_level_preprocess_data(mock_init, sample_data):
    from qml_framework.data_processing import preprocess_data
    result = preprocess_data(sample_data, method='standardize')
    assert isinstance(result, np.ndarray)

@patch('qml_framework.data_processing.initialize_framework')
def test_module_level_extract_features(mock_init, sample_data):
    from qml_framework.data_processing import extract_features
    result = extract_features(sample_data)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_data.shape

@patch('qml_framework.data_processing.initialize_framework')
def test_module_level_process_android_data(mock_init, sample_sensory_data):
    from qml_framework.data_processing import process_android_sensory_data
    result = process_android_sensory_data(sample_sensory_data)
    assert isinstance(result, dict)
    assert 'processed' in result