import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
from src.quantum_sensors.entanglement_handler import EntanglementHandler
from src.quantum_sensors.models import SensorReading

class TestEntanglementHandler:
    
    @pytest.fixture
    def entanglement_handler(self):
        return EntanglementHandler()
    
    @pytest.fixture
    def sample_visual_data(self):
        return SensorReading(
            sensor_id="visual_1",
            timestamp=1234567890,
            data={"intensity": 0.8, "frequency": 100}
        )
    
    @pytest.fixture
    def sample_tactile_data(self):
        return SensorReading(
            sensor_id="tactile_1",
            timestamp=1234567890,
            data={"pressure": 0.5, "temperature": 25.0}
        )
    
    def test_correlate_sensors_success(self, entanglement_handler, sample_visual_data, sample_tactile_data):
        # Arrange
        with patch('src.quantum_sensors.entanglement_handler.fuse_sensors') as mock_fuse_sensors, \
             patch('src.quantum_sensors.entanglement_handler.ZenoProcessor') as mock_zeno_processor, \
             patch('src.quantum_sensors.entanglement_handler.CodonicProcessor') as mock_codonic_processor, \
             patch('src.utils.validate_sensor_data', return_value=True), \
             patch('src.utils.normalize_quantum_states') as mock_normalize:
            
            mock_fusion_data = {"fused": "data"}
            mock_fuse_sensors.return_value = mock_fusion_data
            
            mock_zeno_instance = Mock()
            mock_zeno_processor.return_value = mock_zeno_instance
            mock_stabilized_data = {"stabilized": "data"}
            mock_zeno_instance.apply_zeno_stabilization.return_value = mock_stabilized_data
            
            mock_codonic_instance = Mock()
            mock_codonic_processor.return_value = mock_codonic_instance
            mock_codonic_data = {"processed": "data"}
            mock_codonic_instance.process_codonic_layer.return_value = mock_codonic_data
            
            # Act
            result = entanglement_handler.correlate_sensors(sample_visual_data, sample_tactile_data)
            
            # Assert
            assert result is not None
            assert "entangled_output" in result
            assert "stabilized_data" in result
            assert "codonic_data" in result
            assert "processed_data" in result
    
    def test_correlate_sensors_with_invalid_visual_data(self, entanglement_handler, sample_visual_data, sample_tactile_data):
        # Arrange
        with patch('src.utils.validate_sensor_data', side_effect=[False, True]):  # First visual data invalid
            # Act & Assert
            with pytest.raises(ValueError, match="Invalid sensor data provided."):
                entanglement_handler.correlate_sensors(sample_visual_data, sample_tactile_data)
    
    def test_correlate_sensors_with_invalid_tactile_data(self, entanglement_handler, sample_visual_data, sample_tactile_data):
        # Arrange
        with patch('src.utils.validate_sensor_data', side_effect=[True, False]):  # Second (tactile) data invalid
            # Act & Assert
            with pytest.raises(ValueError, match="Invalid sensor data provided."):
                entanglement_handler.correlate_sensors(sample_visual_data, sample_tactile_data)
    
    def test_correlate_sensors_with_both_invalid_data(self, entanglement_handler, sample_visual_data, sample_tactile_data):
        # Arrange
        with patch('src.utils.validate_sensor_data', return_value=False):
            # Act & Assert
            with pytest.raises(ValueError, match="Invalid sensor data provided."):
                entanglement_handler.correlate_sensors(sample_visual_data, sample_tactile_data)
    
    def test_correlate_sensors_with_mocks_returning_none(self, entanglement_handler, sample_visual_data, sample_tactile_data):
        # Arrange
        with patch('src.utils.validate_sensor_data', return_value=True) as mock_validate, \
             patch('src.quantum_sensors.entanglement_handler.fuse_sensors') as mock_fuse_sensors:
            
            mock_fuse_sensors.return_value = {}
            
            # Act
            result = entanglement_handler.correlate_sensors(sample_visual_data, sample_tactile_data)
            
            # Assert
            assert result is not None
    
    def test_correlate_sensors_empty_data(self, entanglement_handler):
        # Arrange
        empty_visual = SensorReading(sensor_id="", timestamp=0, data={})
        empty_tactile = SensorReading(sensor_id="", timestamp=0, data={})
        
        with patch('src.utils.validate_sensor_data', return_value=True), \
             patch('src.quantum_sensors.entanglement_handler.fuse_sensors') as mock_fuse_sensors:
            
            mock_fuse_sensors.return_value = {}
            
            # Act
            result = entanglement_handler.correlate_sensors(empty_visual, empty_tactile)
            
            # Assert
            assert result is not None
            assert "entangled_output" in result
    
    def test_correlate_sensors_none_inputs(self, entanglement_handler):
        # Arrange
        with patch('src.utils.validate_sensor_data', return_value=False):
            # Act & Assert
            with pytest.raises(ValueError):
                entanglement_handler.correlate_sensors(None, None)
    
    @pytest.mark.parametrize("visual_data,tactile_data", [
        (None, SensorReading(sensor_id="t1", timestamp=1, data={})),
        (SensorReading(sensor_id="v1", timestamp=1, data={}), None),
        (None, None)
    ])
    def test_correlate_sensors_null_inputs(self, entanglement_handler, visual_data, tactile_data):
        # Arrange & Act
        if visual_data is None and tactile_data is None:
            with pytest.raises(ValueError):
                entanglement_handler.correlate_sensors(visual_data, tactile_data)
        elif visual_data is None or tactile_data is None:
            with pytest.raises(Exception):  # Will fail due to None inputs
                entanglement_handler.correlate_sensors(visual_data, tactile_data)
    
    def test_correlate_sensors_with_exception_in_fusion(self, entanglement_handler, sample_visual_data, sample_tactile_data):
        # Arrange
        with patch('src.utils.validate_sensor_data', return_value=True), \
             patch('src.quantum_sensors.entanglement_handler.fuse_sensors') as mock_fuse:
            
            mock_fuse.side_effect = Exception("Fusion error")
            
            # Act & Assert
            with pytest.raises(Exception, match="Fusion error"):
                entanglement_handler.correlate_sensors(sample_visual_data, sample_tactile_data)