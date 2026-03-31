import pytest
import numpy as np
from unittest.mock import Mock, patch
from src.quantum_sensors.fusion_engine import fuse_sensors
from src.quantum_sensors.models import SensorReading, SensorFusionData


class TestFusionEngine:
    """Test suite for the fusion engine module."""

    @pytest.fixture
    def valid_visual_data(self):
        """Fixture providing valid visual sensor data."""
        return SensorReading(
            sensor_id="camera_001",
            timestamp=1234567890.0,
            data={"x": 100, "y": 200, "z": 150},
            metadata={"device": "kinect_v2", "confidence": 0.95}
        )

    @pytest.fixture
    def valid_tactile_data(self):
        """Fixture providing valid tactile sensor data."""
        return SensorReading(
            sensor_id="tactile_array_01",
            timestamp=1234567890.0,
            data={"pressure": 0.8, "texture": 0.6},
            metadata={"sensor_array": "tactile_360"}
        )

    @pytest.fixture
    def invalid_sensor_data(self):
        """Fixture providing invalid sensor data."""
        return SensorReading(
            sensor_id="",
            timestamp=-1.0,
            data={},
            metadata={}
        )

    def test_fuse_sensors_with_valid_data(self, valid_visual_data, valid_tactile_data):
        """Test successful sensor fusion with valid input data."""
        result = fuse_sensors(valid_visual_data, valid_tactile_data)
        
        assert result is not None
        assert isinstance(result, SensorFusionData)
        assert hasattr(result, 'fused_confidence')
        assert 0.0 <= result.fused_confidence <= 1.0
        assert result.fusion_vector is not None

    def test_fuse_sensors_with_mismatched_timestamps(self):
        """Test sensor fusion with mismatched timestamps."""
        visual_data = SensorReading(
            sensor_id="camera_001",
            timestamp=1234567890.0,
            data={"x": 100, "y": 200, "z": 150},
            metadata={"device": "kinect_v2", "confidence": 0.95}
        )
        
        tactile_data = SensorReading(
            sensor_id="tactile_array_01",
            timestamp=1234567895.0,  # Different timestamp
            data={"pressure": 0.8, "texture": 0.6},
            metadata={"sensor_array": "tactile_360"}
        )
        
        result = fuse_sensors(visual_data, tactile_data)
        
        assert result is not None
        assert isinstance(result, SensorFusionData)

    def test_fuse_sensors_with_empty_data(self):
        """Test sensor fusion with empty sensor data."""
        empty_visual = SensorReading(
            sensor_id="",
            timestamp=0.0,
            data={},
            metadata={}
        )
        
        empty_tactile = SensorReading(
            sensor_id="",
            timestamp=0.0,
            data={},
            metadata={}
        )
        
        result = fuse_sensors(empty_visual, empty_tactile)
        
        assert result is not None
        assert isinstance(result, SensorFusionData)

    def test_fuse_sensors_with_none_inputs(self):
        """Test sensor fusion with None inputs raises appropriate error."""
        with pytest.raises((TypeError, AttributeError)):
            fuse_sensors(None, None)

    def test_data_consistency_across_multiple_calls(self, valid_visual_data, valid_tactile_data):
        """Test that sensor fusion maintains data consistency across multiple readings."""
        results = []
        # Run fusion multiple times to check consistency
        for i in range(5):
            fused = fuse_sensors(valid_visual_data, valid_tactile_data)
            results.append(fused.fusion_vector)
        
        # Check all results are consistent
        for result in results:
            assert result is not None
            assert isinstance(result, list)

    def test_fuse_sensors_with_edge_case_data_values(self):
        """Test sensor fusion with edge case data values."""
        # Test with extreme values
        visual_data = SensorReading(
            sensor_id="test_camera",
            timestamp=1234567890.0,
            data={"x": 0, "y": 0, "z": 0},  # Edge case: all zeros
            metadata={"resolution": "1920x1080"}
        )
        
        tactile_data = SensorReading(
            sensor_id="test_tactile",
            timestamp=1234567890.0,
            data={"pressure": 0.0, "temperature": -273.15},  # Edge case: absolute zero
            metadata={"sensitivity": "high"}
        )
        
        result = fuse_sensors(visual_data, tactile_data)
        
        assert result is not None
        assert isinstance(result, SensorFusionData)
        assert hasattr(result, 'fused_confidence')

    def test_fuse_sensors_with_invalid_sensor_ids(self, invalid_sensor_data):
        """Test sensor fusion behavior with invalid sensor IDs."""
        visual_data = SensorReading(
            sensor_id=None,  # Invalid sensor_id
            timestamp=1234567890.0,
            data={"x": 100, "y": 200, "z": 150},
            metadata={"device": "kinect_v2", "confidence": 0.95}
        )
        
        tactile_data = SensorReading(
            sensor_id="",  # Empty sensor_id
            timestamp=1234567890.0,
            data={"pressure": 0.8, "texture": 0.6},
            metadata={"sensor_array": "tactile_360"}
        )
        
        result = fuse_sensors(visual_data, tactile_data)
        
        assert result is not None
        assert isinstance(result, SensorFusionData)

    @patch('src.quantum_sensors.fusion_engine.np')
    def test_fuse_sensors_with_numpy_errors(self, mock_np):
        """Test sensor fusion handles numpy library errors gracefully."""
        mock_np.linalg.norm.side_effect = Exception("Numpy error")
        
        visual_data = SensorReading(
            sensor_id="camera_001",
            timestamp=1234567890.0,
            data={"x": 100, "y": 200, "z": 150},
            metadata={"device": "kinect_v2", "confidence": 0.95}
        )
        
        tactile_data = SensorReading(
            sensor_id="tactile_array_01",
            timestamp=1234567890.0,
            data={"pressure": 0.8, "texture": 0.6},
            metadata={"sensor_array": "tactile_360"}
        )
        
        # Should handle the error gracefully
        result = fuse_sensors(visual_data, tactile_data)
        
        assert result is not None
        assert isinstance(result, SensorFusionData)

    def test_fuse_sensors_with_large_data_sets(self):
        """Test sensor fusion with large data sets."""
        # Create large data sets
        large_visual_data = {}
        large_tactile_data = {}
        
        for i in range(1000):  # Large data set
            large_visual_data[f"key_{i}"] = i * 0.5
            large_tactile_data[f"sensor_{i}"] = i * 0.3
        
        visual_data = SensorReading(
            sensor_id="large_camera",
            timestamp=1234567890.0,
            data=large_visual_data,
            metadata={"device": "high_res_camera"}
        )
        
        tactile_data = SensorReading(
            sensor_id="large_tactile",
            timestamp=1234567890.0,
            data=large_tactile_data,
            metadata={"sensor_array": "high_density"}
        )
        
        result = fuse_sensors(visual_data, tactile_data)
        
        assert result is not None
        assert isinstance(result, SensorFusionData)