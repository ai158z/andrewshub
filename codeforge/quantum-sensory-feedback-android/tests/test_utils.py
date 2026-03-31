import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.utils import validate_sensor_data, normalize_quantum_states, process_sensor_fusion, apply_zeno_stabilization
from src.quantum_sensors.models import SensorReading, SensorFusionData

class TestValidateSensorData:
    """Test suite for validate_sensor_data function"""
    
    def test_valid_sensor_data(self):
        """Test validation of valid sensor data"""
        data = {
            'sensor_id': 'sensor123',
            'values': [25.0, 30.0, 35.0],
            'timestamp': 1234567890
        }
        result = validate_sensor_data(data)
        assert result is True
    
    def test_invalid_sensor_data_missing_fields(self):
        """Test validation fails with missing required fields"""
        # Test missing sensor_id
        data = {
            'values': [25.0, 30.0, 35.0],
            'timestamp': 1234567890
        }
        result = validate_sensor_data(data)
        assert result is False
    
    def test_invalid_sensor_data_wrong_types(self):
        """Test validation fails with wrong data types"""
        data = {
            'sensor_id': 123,  # Should be string
            'values': [25.0, 30.0, 35.0],
            'timestamp': 'invalid'  # Should be int/float
        }
        result = validate_sensor_data(data)
        assert result is False
    
    def test_invalid_sensor_data_values_out_of_range(self):
        """Test validation handles out of range values"""
        data = {
            'sensor_id': 'sensor123',
            'values': [150.0, -10.0, 35.0],  # Values out of 0-100 range
            'timestamp': 1234567890
        }
        result = validate_sensor_data(data)
        # Function should return False for validation failure
        assert result is False

class TestNormalizeQuantumStates:
    """Test suite for normalize_quantum_states function"""
    
    def test_normalize_valid_data(self):
        """Test normalization with valid data"""
        data = [0.5, 0.3, 0.2]
        result = normalize_quantum_states(data)
        expected_sum = 1.0
        assert abs(sum(result) - expected_sum) < 1e-10
    
    def test_normalize_empty_data(self):
        """Test normalization with empty data"""
        data = []
        result = normalize_quantum_states(data)
        assert result == []
    
    def test_normalize_invalid_values(self):
        """Test normalization with invalid values"""
        data = [float('inf'), float('nan'), 0.5]
        with pytest.raises(ValueError):
            normalize_quantum_states(data)
    
    def test_normalize_negative_values(self):
        """Test normalization preserves non-negative values"""
        data = [-0.5, -0.3, 0.2]
        # Should handle negative values gracefully
        with pytest.raises(ValueError):
            normalize_quantum_states(data)

class TestProcessSensorFusion:
    """Test suite for process_sensor_fusion function"""
    
    @patch('src.utils.normalize_quantum_states')
    @patch('src.utils.SensorFusionData')
    def test_process_fusion_valid_data(self, mock_fusion_data, mock_normalize):
        """Test processing valid fusion data"""
        visual_reading = SensorReading(sensor_id="vis1", values=[0.5, 0.3, 0.2], timestamp=1234567890)
        tactile_reading = SensorReading(sensor_id="tac1", values=[0.4, 0.4, 0.2], timestamp=1234567890)
        
        mock_normalize.side_effect = lambda x: x
        mock_fusion_data.return_value = MagicMock()
        
        result = process_sensor_fusion(visual_reading, tactile_reading)
        assert result is not None
    
    def test_process_fusion_invalid_data(self):
        """Test processing with invalid data"""
        visual_reading = None
        tactile_reading = None
        
        with pytest.raises(ValueError):
            process_sensor_fusion(visual_reading, tactile_reading)

class TestApplyZenoStabilization:
    """Test suite for apply_zeno_stabilization function"""
    
    def test_zeno_stabilization_valid_data(self):
        """Test Zeno stabilization with valid data"""
        data = [0.5, 0.3, 0.2]
        result = apply_zeno_stabilization(data)
        # Should return stabilized values
        assert result is not None
    
    def test_zeno_stabilization_empty_data(self):
        """Test Zeno stabilization with empty data"""
        data = []
        result = apply_zeno_stabilization(data)
        assert result == []
    
    @pytest.mark.parametrize("data", [
        [float('inf'), 1.0, 2.0],
        [float('nan'), 1.0, 2.0]
    ])
    def test_zeno_stabilization_invalid_values(self, data):
        """Test Zeno stabilization with invalid values"""
        with pytest.raises(ValueError):
            apply_zeno_stabilization(data)