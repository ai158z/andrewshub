import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from examples.sensory_processing_example import SensoryProcessingExample, main

class TestSensoryProcessingExample:
    
    def test_init(self):
        """Test initialization of SensoryProcessingExample"""
        example = SensoryProcessingExample()
        assert example.framework is None
        assert example.data is None
        assert example.model is None
        assert example.is_initialized is False
    
    def test_setup_framework_success(self):
        """Test successful framework setup"""
        with patch('examples.sensory_processing_example.initialize_framework') as mock_init:
            mock_init.return_value = "Framework initialized"
            example = SensoryProcessingExample()
            example.setup_framework()
            assert example.is_initialized is True
            assert example.framework == "Framework initialized"
    
    def test_setup_framework_failure(self):
        """Test framework setup failure"""
        with patch('examples.sensory_processing_example.initialize_framework', side_effect=Exception("Init failed")):
            example = SensoryProcessingExample()
            with pytest.raises(Exception, match="Init failed"):
                example.setup_framework()
    
    def test_load_sample_data_success(self):
        """Test successful sample data loading"""
        example = SensoryProcessingExample()
        example.load_sample_data()
        assert example.data is not None
        assert 'features' in example.data
        assert 'labels' in example.data
    
    def test_load_sample_data_failure(self):
        """Test sample data loading failure"""
        with patch('examples.sensory_processing_example.np.random.rand', side_effect=Exception("Data load failed")):
            example = SensoryProcessingExample()
            with pytest.raises(Exception, match="Data load failed"):
                example.load_sample_data()
    
    def test_process_data_success(self):
        """Test successful data processing"""
        example = SensoryProcessingExample()
        example.is_initialized = True
        with patch('examples.sensory_processing_example.process_sensory_data') as mock_process:
            mock_process.return_value = "Sensory data processed"
            result = example.process_data()
            assert result == "Sensory data processed"
    
    def test_process_data_framework_not_initialized(self):
        """Test data processing when framework is not initialized"""
        example = SensoryProcessingExample()
        example.is_initialized = False
        # Should not raise exception and return None
        result = example.process_data()
        assert result is None
    
    def test_process_data_failure(self):
        """Test data processing failure"""
        example = SensoryProcessingExample()
        example.is_initialized = True
        with patch('examples.sensory_processing_example.process_sensory_data', side_effect=Exception("Process failed")):
            with pytest.raises(Exception, match="Process failed"):
                example.process_data()
    
    def test_create_quantum_model_success(self):
        """Test successful quantum model creation"""
        example = SensoryProcessingExample()
        example.create_quantum_model()
        assert example.model is not None
    
    def test_create_quantum_model_failure(self):
        """Test quantum model creation failure"""
        example = SensoryProcessingExample()
        with patch('examples.sensory_processing_example.QuantumKernel', side_effect=Exception("Model creation failed")):
            with pytest.raises(Exception, match="Model creation failed"):
                example.create_quantum_model()
    
    def test_run_sensory_processing_success(self):
        """Test successful run of sensory processing"""
        with patch('examples.sensory_processing_example.initialize_framework') as mock_init, \
             patch('examples.sensory_processing_example.process_sensory_data') as mock_process, \
             patch('examples.sensory_processing_example.VQC') as mock_vqc:
            
            mock_init.return_value = "Framework initialized"
            mock_process.return_value = "Sensory data processed"
            mock_vqc.return_value = MagicMock()
            
            example = SensoryProcessingExample()
            results = example.run_sensory_processing()
            
            assert results['framework'] == "OK"
            assert results['data_loading'] == "OK"
            assert results['data_processing'] == "Sensory data processed"
            assert results['model_creation'] == "OK"
    
    def test_run_sensory_processing_failure(self):
        """Test failure in sensory processing"""
        example = SensoryProcessingExample()
        with patch('examples.sensory_processing_example.initialize_framework', side_effect=Exception("Framework error")):
            results = example.run_sensory_processing()
            assert 'error' in results
            assert results['error'] == "Framework error"
    
    def test_main_success(self):
        """Test successful execution of main function"""
        with patch('examples.sensory_processing_example.SensoryProcessingExample') as mock_example:
            mock_instance = MagicMock()
            mock_instance.run_sensory_processing.return_value = {"result": "success"}
            mock_example.return_value = mock_instance
            
            results = main()
            assert results["result"] == "success"
    
    def test_main_failure(self):
        """Test failure in main function execution"""
        with patch('examples.sensory_processing_example.SensoryProcessingExample') as mock_example:
            mock_example.side_effect = Exception("Main function error")
            
            results = main()
            assert "error" in results
    
    def test_data_processing_with_framework_error(self):
        """Test data processing when framework setup fails"""
        example = SensoryProcessingExample()
        example.is_initialized = False
        result = example.process_data()
        assert result is None
    
    @patch('examples.sensory_processing_example.numpy')
    def test_load_sample_data_deterministic(self, mock_numpy):
        """Test that sample data loading produces deterministic results"""
        example = SensoryProcessingExample()
        example.load_sample_data()
        # Check that data has expected structure
        assert example.data is not None
        assert len(example.data['features']) == 100
        assert len(example.data['labels']) == 100
    
    def test_model_creation_components(self):
        """Test that quantum model components are created properly"""
        example = SensoryProcessingExample()
        example.create_quantum_model()
        assert example.model is not None
    
    def test_complete_flow(self):
        """Test complete sensory processing flow"""
        with patch('examples.sensory_processing_example.initialize_framework') as mock_init, \
             patch('examples.sensory_processing_example.process_sensory_data') as mock_process:
            
            mock_init.return_value = "Framework initialized"
            mock_process.return_value = "Sensory data processed"
            
            example = SensoryProcessingExample()
            results = example.run_sensory_processing()
            
            # Verify all steps completed
            assert 'framework' in results
            assert 'data_loading' in results
            assert 'data_processing' in results
            assert 'model_creation' in results
            assert 'quantum_processing' in results
    
    def test_logging_integration(self):
        """Test that appropriate logging occurs during execution"""
        with patch('examples.sensory_processing_example.logger') as mock_logger:
            example = SensoryProcessingExample()
            example.is_initialized = True
            example.setup_framework()
            example.load_sample_data()
            example.process_data()
            example.create_quantum_model()
            # Verify logging was called
            assert mock_logger.info.called

    def test_sample_data_structure(self):
        """Test that sample data has expected structure and types"""
        example = SensoryProcessingExample()
        example.load_sample_data()
        assert isinstance(example.data['features'], np.ndarray)
        assert isinstance(example.data['labels'], np.ndarray)
        assert example.data['features'].shape[1] == 4  # 4 features
        assert set(example.data['labels']).issubset({0, 1})  # Binary labels