import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any
from src.quantum_sensors.fusion_engine import FusionEngine, fuse_sensors
from src.quantum_sensors.models import SensorFusionData

class TestFusionEngine:
    """Test suite for the FusionEngine class"""
    
    @pytest.fixture
    def fusion_engine(self):
        """Fixture to provide a FusionEngine instance with mocked dependencies"""
        engine = FusionEngine()
        # Mock the dependencies to avoid external calls
        with patch.multiple(engine, 
                         config_manager=Mock(),
                         zeno_processor=Mock(),
                         codonic_processor=Mock(),
                         entanglement_handler=Mock()):
            yield engine
    
    @pytest.fixture
    def valid_visual_data(self):
        """Valid visual sensor data for testing"""
        return {
            "timestamp": "2023-01-01T12:00:00Z",
            "data": {"intensity": 0.5, "frequency": 100},
            "metadata": {"sensor_id": "vis_001"}
        }
    
    @pytest.fixture
    def valid_tactile_data(self):
        """Valid tactile sensor data for testing"""
        return {
            "timestamp": "2023-01-01T12:00:00Z",
            "data": {"pressure": 15.5, "texture": "smooth"},
            "metadata": {"sensor_id": "tac_001"}
        }
    
    @pytest.fixture
    def invalid_sensor_data(self):
        """Invalid sensor data that should fail validation"""
        return {
            "invalid": "data",
            "missing_required_fields": True
        }

    def test_fuse_sensors_success(self, fusion_engine, valid_visual_data, valid_tactile_data):
        """Test successful sensor fusion with valid data"""
        # Mock the processing steps
        fusion_engine.codonic_processor.process_codonic_layer = Mock(return_value=valid_visual_data)
        fusion_engine.entanglement_handler.correlate_sensors = Mock(return_value=valid_visual_data)
        fusion_engine.zeno_processor.apply_zeno_stabilization = Mock(return_value=valid_visual_data)
        
        result = fusion_engine.fuse_sensors(valid_visual_data, valid_tactile_data)
        
        assert isinstance(result, SensorFusionData)
        assert result.timestamp == valid_visual_data.get('timestamp', '')
        assert "processing_steps" in result.fusion_metadata
        
    def test_fuse_sensors_with_invalid_visual_data(self, fusion_engine, valid_tactile_data, invalid_sensor_data):
        """Test sensor fusion with invalid visual data"""
        with patch('src.quantum_sensors.fusion_engine.validate_sensor_data', side_effect=Exception("Invalid visual data")):
            with pytest.raises(RuntimeError, match="Failed to fuse sensors"):
                fusion_engine.fuse_sensors(invalid_sensor_data, valid_tactile_data)
    
    def test_fuse_sensors_with_invalid_tactile_data(self, fusion_engine, valid_visual_data, invalid_sensor_data):
        """Test sensor fusion with invalid tactile data"""
        with patch('src.quantum_sensors.fusion_engine.validate_sensor_data', side_effect=Exception("Invalid tactile data")):
            with pytest.raises(RuntimeError, match="Failed to fuse sensors"):
                fusion_engine.fuse_sensors(valid_visual_data, invalid_sensor_data)
    
    @pytest.mark.parametrize("visual_data,tactile_data,expected_error", [
        (None, {"valid": "data"}, "Failed to fuse sensors: 'NoneType' object has no attribute"),
        ({"valid": "data"}, None, "Failed to fuse sensors: 'NoneType' object has no attribute"),
        (None, None, "Failed to fuse sensors: 'NoneType' object has no attribute")
    ])
    def test_fuse_sensors_with_none_inputs(self, fusion_engine, visual_data, tactile_data, expected_error):
        """Test sensor fusion with None inputs"""
        with pytest.raises(RuntimeError, match=expected_error):
            fusion_engine.fuse_sensors(visual_data, tactile_data)
            
    def test_fuse_sensors_processing_steps(self, fusion_engine, valid_visual_data, valid_tactile_data):
        """Test that all processing steps are recorded in metadata"""
        # Mock all the processing steps to return predictable data
        fusion_engine.codonic_processor.process_codonic_layer = Mock(return_value=valid_visual_data)
        fusion_engine.entanglement_handler.correlate_sensors = Mock(return_value=valid_visual_data)
        fusion_engine.zeno_processor.apply_zeno_stabilization = Mock(return_value=valid_visual_data)
        
        result = fusion_engine.fuse_sensors(valid_visual_data, valid_tactile_data)
        
        expected_steps = [
            "data_validation",
            "quantum_normalization", 
            "codonic_processing",
            "entanglement_correlation",
            "zeno_stabilization"
        ]
        assert result.fusion_metadata["processing_steps"] == expected_steps

    def test_module_level_fuse_sensors_function(self, valid_visual_data, valid_tactile_data):
        """Test the module-level fuse_sensors function"""
        # Mock the internal FusionEngine to avoid actual processing
        with patch('src.quantum_sensors.fusion_engine.FusionEngine') as mock_engine_class:
            mock_engine = Mock()
            mock_engine.fuse_sensors.return_value = Mock(spec=SensorFusionData)
            mock_engine_class.return_value = mock_engine
            
            # Call the module-level function
            result = fuse_sensors(valid_visual_data, valid_tactile_data)
            
            # Verify the engine was instantiated and method was called
            mock_engine_class.assert_called()
            mock_engine.fuse_sensors.assert_called_once_with(valid_visual_data, valid_tactile_data)
            assert result is not None

    def test_fuse_sensors_exception_handling(self, fusion_engine, valid_visual_data, valid_tactile_data):
        """Test that exceptions during processing are handled properly"""
        # Make the first validation fail
        with patch('src.quantum_sensors.fusion_engine.validate_sensor_data', side_effect=Exception("Validation failed")):
            with pytest.raises(RuntimeError, match="Failed to fuse sensors: Validation failed"):
                fusion_engine.fuse_sensors(valid_visual_data, valid_tactile_data)

    def test_normalize_quantum_states_called(self, fusion_engine, valid_visual_data, valid_tactile_data):
        """Test that normalize_quantum_states is called during processing"""
        with patch('src.quantum_sensors.fusion_engine.normalize_quantum_states') as mock_normalize:
            mock_normalize.return_value = valid_visual_data
            fusion_engine.codonic_processor.process_codonic_layer = Mock(return_value=valid_visual_data)
            fusion_engine.entanglement_handler.correlate_sensors = Mock(return_value=valid_visual_data)
            fusion_engine.zeno_processor.apply_zeno_stabilization = Mock(return_value=valid_visual_data)
            
            fusion_engine.fuse_sensors(valid_visual_data, valid_tactile_data)
            
            # Verify normalize was called for both inputs
            assert mock_normalize.call_count == 2
            calls = mock_normalize.call_args_list
            assert len(calls) == 2
            # First call should be visual_data, second should be tactile_data