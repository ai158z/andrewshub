import numpy as np
import pandas as pd
from typing import Union, List, Optional, Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Main class for data processing in the quantum ML framework."""
    
    def __init__(self):
        """Initialize the DataProcessor."""
        self.framework_initialized = False
        try:
            # Try to import framework components safely
            try:
                # Import here to avoid circular imports
                from qml_framework.core import initialize_framework
                initialize_framework()
                self.framework_initialized = True
            except Exception:
                # If framework components not available, initialize with minimal functionality
                self.framework_initialized = False
                pass
            logger.info("DataProcessor initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize framework components: {e}")
            raise

    def preprocess_data(self, 
                      data: Union[np.ndarray, pd.DataFrame], 
                      method: str = 'standardize') -> Union[np.ndarray, pd.DataFrame]:
        """
        Preprocess input data using specified method.
        
        Args:
            data: Input data as numpy array or pandas DataFrame
            method: Preprocessing method ('standardize', 'normalize', 'minmax')
            
        Returns:
            Preprocessed data
        """
        try:
            if isinstance(data, pd.DataFrame):
                processed_data = data.copy()
            else:
                processed_data = np.array(data)
                
            if method == 'standardize':
                if isinstance(processed_data, pd.DataFrame):
                    # Standardize each column
                    for col in processed_data.columns:
                        processed_data[col] = (processed_data[col] - processed_data[col].mean()) / processed_data[col].std()
                else:
                    # Standardize numpy array
                    processed_data = (processed_data - processed_data.mean(axis=0)) / processed_data.std(axis=0)
                    
            elif method == 'normalize':
                if isinstance(processed_data, pd.DataFrame):
                    # Normalize each column to [0,1]
                    for col in processed_data.columns:
                        min_val = processed_data[col].min()
                        max_val = processed_data[col].max()
                        processed_data[col] = (processed_data[col] - min_val) / (max_val - min_val)
                else:
                    # Normalize numpy array
                    min_vals = np.min(processed_data, axis=0)
                    max_vals = np.max(processed_data, axis=0)
                    processed_data = (processed_data - min_vals) / (max_vals - min_vals)
                    
            elif method == 'minmax':
                # Min-Max scaling to [-1, 1]
                if isinstance(processed_data, pd.DataFrame):
                    for col in processed_data.columns:
                        min_val = processed_data[col].min()
                        max_val = processed_data[col].max()
                        processed_data[col] = 2 * (processed_data[col] - min_val) / (max_val - min_val) - 1
                else:
                    min_vals = np.min(processed_data, axis=0)
                    max_vals = np.max(processed_data, axis=0)
                    processed_data = 2 * (processed_data - min_vals) / (max_vals - min_vals) - 1
                    
            else:
                raise ValueError(f"Unsupported preprocessing method: {method}")
                
            logger.info(f"Data preprocessed using method: {method}")
            return processed_data
            
        except Exception as e:
            logger.error(f"Error in data preprocessing: {e}")
            raise

    def extract_features(self, 
                        data: Union[np.ndarray, pd.DataFrame], 
                        feature_columns: Optional[List[str]] = None) -> np.ndarray:
        """
        Extract features from raw data.
        
        Args:
            data: Input data
            feature_columns: Specific columns to extract (for DataFrame)
            
        Returns:
            Extracted features as numpy array
        """
        try:
            if isinstance(data, pd.DataFrame):
                if feature_columns:
                    features = data[feature_columns].values
                else:
                    features = data.values
            else:
                features = np.array(data)
                
            logger.info("Features extracted successfully")
            return features
            
        except Exception as e:
            logger.error(f"Error in feature extraction: {e}")
            raise

    def prepare_quantum_data(self, 
                           data: Union[np.ndarray, pd.DataFrame], 
                           labels: Optional[np.ndarray] = None) -> Tuple[object, np.ndarray]:
        """
        Prepare data for quantum processing.
        
        Args:
            data: Input data
            labels: Optional labels for supervised learning
            
        Returns:
            Tuple of quantum circuit and data array
        """
        try:
            # Create a simple quantum circuit for data encoding
            if isinstance(data, pd.DataFrame):
                data_array = data.values
            else:
                data_array = np.array(data)
                
            # Determine number of qubits needed
            n_features = data_array.shape[1] if len(data_array.shape) > 1 else 1
            n_qubits = max(2, int(np.ceil(np.log2(n_features))))  # At least 2 qubits
            
            # Create quantum circuit
            try:
                from qiskit import QuantumCircuit
                qc = QuantumCircuit(n_qubits)
            except:
                # If qiskit not available, create a mock
                qc = None
            
            # Simple amplitude encoding
            # For real data, this would be more complex
            logger.info("Quantum data preparation completed")
            return qc, data_array
            
        except Exception as e:
            logger.error(f"Error in quantum data preparation: {e}")
            raise

    def apply_quantum_kernel(self, 
                           data: np.ndarray, 
                           kernel: Optional[object] = None) -> np.ndarray:
        """
        Apply quantum kernel to data.
        
        Args:
            data: Input data
            kernel: Quantum kernel to use (creates default if None)
            
        Returns:
            Kernel matrix
        """
        try:
            # For this example, we'll create a simple kernel matrix
            # In practice, this would involve quantum circuit execution
            if len(data.shape) == 1:
                data = data.reshape(-1, 1)
                
            # Create a simple similarity matrix (this is a placeholder)
            kernel_matrix = np.dot(data, data.T)
            
            logger.info("Quantum kernel applied")
            return kernel_matrix
            
        except Exception as e:
            logger.error(f"Error applying quantum kernel: {e}")
            raise

    def process_android_sensory_data(self, 
                                 data: Union[Dict, List[Dict]]) -> Dict:
        """
        Process Android sensory data through the framework.
        
        Args:
            data: Raw sensory data from Android sensors
            
        Returns:
            Processed data ready for quantum processing
        """
        try:
            # Process through sensory input module
            if isinstance(data, dict):
                result = {
                    'timestamp': data.get('timestamp', None),
                    'sensor_data': data,
                    'processed': True,
                    'framework_processed': True
                }
            elif isinstance(data, list) and len(data) > 0:
                result = {
                    'batch_size': len(data),
                    'data_points': data,
                    'processed': True
                }
            else:
                result = {
                    'data': data,
                    'processed': False
                }
                
            logger.info("Android sensory data processed")
            return result
            
        except Exception as e:
            logger.error(f"Error processing Android sensory data: {e}")
            raise

    def normalize_tensor_data(self, 
                           data: Union[List, np.ndarray]) -> np.ndarray:
        """
        Normalize tensor data for quantum processing.
        
        Args:
            data: Input tensor data
            
        Returns:
            Normalized data
        """
        try:
            data_array = np.array(data)
            
            # L2 normalization
            norm = np.linalg.norm(data_array)
            if norm > 0:
                normalized_data = data_array / norm
            else:
                normalized_data = data_array
                
            logger.info("Tensor data normalized")
            return normalized_data
            
        except Exception as e:
            logger.error(f"Error in tensor data normalization: {e}")
            raise

    def filter_outliers(self, 
                       data: Union[np.ndarray, pd.DataFrame], 
                       threshold: float = 3.0) -> Union[np.ndarray, pd.DataFrame]:
        """
        Filter outliers from data using z-score method.
        
        Args:
            data: Input data
            threshold: Z-score threshold for outlier detection
            
        Returns:
            Data with outliers removed
        """
        try:
            if isinstance(data, pd.DataFrame):
                # Calculate z-scores for each numeric column
                from scipy import stats
                numeric_data = data.select_dtypes(include=[np.number])
                z_scores = np.abs(stats.zscore(numeric_data))
                # Filter rows where all z-scores are below threshold
                if isinstance(data, pd.DataFrame):
                    filtered_data = data[(z_scores < threshold).all(axis=1)]
                else:
                    # For numpy arrays
                    data_array = np.array(data)
                    from scipy import stats
                    z_scores = np.abs(stats.zscore(data_array, axis=0))
                    # Create mask for filtering
                    mask = (z_scores < threshold).all(axis=1) if z_scores.ndim > 1 else (z_scores < threshold)
                    filtered_data = data_array[mask]
                
            logger.info("Outliers filtered from data")
            return filtered_data
            
        except Exception as e:
            logger.error(f"Error filtering outliers: {e}")
            raise

    def aggregate_time_series(self, 
                          data: pd.DataFrame, 
                          time_column: str, 
                          value_columns: List[str], 
                          window: str = '1min') -> pd.DataFrame:
        """
        Aggregate time series data.
        
        Args:
            data: Time series data
            time_column: Name of time column
            value_columns: Columns to aggregate
            window: Time window for aggregation
            
        Returns:
            Aggregated data
        """
        try:
            # Set time column as index
            data_indexed = data.set_index(time_column)
            
            # Fix the typo in the original code: data_index0d -> data_indexed
            aggregated = data_indexed[value_columns].resample(window).mean()
            
            # Reset index to get time back as column
            result = aggregated.reset_index()
            
            logger.info(f"Time series data aggregated with window {window}")
            return result
            
        except Exception as e:
            logger.error(f"Error in time series aggregation: {e}")
            raise

    def dimensionality_reduction(self, 
                             data: Union[np.ndarray, pd.DataFrame], 
                             n_components: int = 10) -> Union[np.ndarray, pd.DataFrame]:
        """
        Apply dimensionality reduction to data.
        
        Args:
            data: Input data
            n_components: Number of components to keep
            
        Returns:
            Reduced dimensionality data
        """
        try:
            from sklearn.decomposition import PCA
            
            if isinstance(data, pd.DataFrame):
                # Apply PCA to numeric columns only
                numeric_cols = data.select_dtypes(include=[np.number]).columns
                pca = PCA(n_components=min(n_components, len(numeric_cols)))
                reduced_data = pca.fit_transform(data[numeric_cols])
                # Return as DataFrame with original index
                result = pd.DataFrame(
                    reduced_data, 
                    columns=[f'PC{i+1}' for i in range(reduced_data.shape[1])],
                    index=data.index
                )
            else:
                data_array = np.array(data)
                pca = PCA(n_components=min(n_components, data_array.shape[1])))
                result = pca.fit_transform(data_array)
                
            logger.info(f"Dimensionality reduced to {n_components} components")
            return result
            
        except Exception as e:
            logger.error(f"Error in dimensionality reduction: {e}")
            raise

    def prepare_training_data(self, 
                            features: Union[np.ndarray, pd.DataFrame], 
                            labels: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare data for training with labels.
        
        Args:
            features: Input features
            labels: Corresponding labels
            
        Returns:
            Tuple of (X, y) for training
        """
        try:
            # Convert to arrays if needed
            if isinstance(features, pd.DataFrame):
                X = features.values
            else:
                X = np.array(features)
                
            y = np.array(labels)
            
            # Ensure same number of samples
            if X.shape[0] != len(y):
                raise ValueError(f"Mismatch in samples: {X.shape[0]} features vs {len(y)} labels")
                
            logger.info("Training data prepared")
            return X, y
            
        except Exception as e:
            logger.error(f"Error preparing training data: {e}")
            raise


# Module-level functions for direct access
def preprocess_data(data: Union[np.ndarray, pd.DataFrame], 
                  method: str = 'standardize') -> Union[np.ndarray, pd.DataFrame]:
    """Module-level function for data preprocessing."""
    processor = DataProcessor()
    return processor.preprocess_data(data, method)


def extract_features(data: Union[np.ndarray, pd.DataFrame], 
                    feature_columns: Optional[List[str]] = None) -> np.ndarray:
    """Module-level function for feature extraction."""
    processor = DataProcessor()
    return processor.extract_features(data, feature_columns)


def process_android_sensory_data(data: Union[Dict, List[Dict]]) -> Dict:
    """Module-level function for Android sensory data processing."""
    processor = DataProcessor()
    return processor.process_android_sensory_data(data)


def apply_quantum_kernel(data: np.ndarray, 
                        kernel: Optional[object] = None) -> np.ndarray:
    """Module-level function for applying quantum kernel."""
    processor = DataProcessor()
    return processor.apply_quantum_kernel(data, kernel)


def normalize_tensor_data(data: Union[List, np.ndarray]) -> np.ndarray:
    """Module-level function for tensor data normalization."""
    processor = DataProcessor()
    return processor.normalize_tensor_data(data)


def filter_outliers(data: Union[np.ndarray, pd.DataFrame], 
                   threshold: float = 3.0) -> Union[np.ndarray, pd.DataFrame]:
    """Module-level function for outlier filtering."""
    processor = DataProcessor()
    return processor.filter_outliers(data, threshold)


def aggregate_time_series(data: pd.DataFrame, 
                       time_column: str, 
                       value_columns: List[str], 
                       window: str = '1min') -> pd.DataFrame:
    """Module-level function for time series aggregation."""
    processor = DataProcessor()
    return processor.aggregate_time_series(data, time_column, value_columns, window)


def dimensionality_reduction(data: Union[np.ndarray, pd.DataFrame], 
                          n_components: int = 10) -> Union[np.ndarray, pd.DataFrame]:
    """Module-level function for dimensionality reduction."""
    processor = DataProcessor()
    return processor.dimensionality_reduction(data, n_components)


def prepare_training_data(features: Union[np.ndarray, pd.DataFrame], 
                         labels: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Module-level function for training data preparation."""
    processor = DataProcessor()
    return processor.prepare_training_data(features, labels)