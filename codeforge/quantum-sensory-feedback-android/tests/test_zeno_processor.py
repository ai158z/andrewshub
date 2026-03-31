import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.quantum_sensors.zeno_processor import ZenoProcessor
from src.quantum_sensors.models import SensorReading, SensorFusionData

class TestZenoProcessor:
    @pytest.fixture
    def zeno_processor(self):
        with patch('src.quantum_sensors.zeno_processor.ConfigManager') as mock_config_manager:
            mock_config = MagicMock()
            mock_config.get.return_value = {'zeno_frequency': 100, 'decoherence_threshold': 0.01}
            mock_config_manager.get_config.return_value = mock_config
            processor = ZenoProcessor()
            processor.config_manager = mock_config_manager
            return processor

    @pytest.fixture
    def sample_sensor_reading(self):
        return SensorReading(
            sensor_id="test_sensor_1",
            value=1.5,
            timestamp=datetime.now()
        )

    @pytest.fixture
    def sample_sensor_fusion_data(self, sample_sensor_reading):
        return SensorFusionData(
            sensor_readings=[sample_sensor_reading],
            fusion_timestamp=datetime.now()
        )

    def test_init_zeno_processor(self):
        with patch('src.quantum_sensors.zeno_processor.ConfigManager') as mock_config_manager:
            mock_config = MagicMock()
            mock_config.get.return_value = {'zeno_frequency': 100, 'decoherence_threshold': 0.01}
            mock_config_manager().get_config.return_value = mock_config
            
            processor = ZenoProcessor()
            
            assert processor.stabilization_frequency == 100
            assert processor.decoherence_threshold == 0.01

    def test_apply_zeno_stabilization_with_valid_data(self, zeno_processor, sample_sensor_fusion_data):
        # Test successful stabilization
        result = zeno_processor.apply_zeno_stabilization(sample_sensor_fusion_data)
        assert isinstance(result, SensorFusionData)
        assert len(result.sensor_readings) == len(sample_sensor_fusion_data.sensor_readings)

    def test_apply_zeno_stabilization_with_none_data(self, zeno_processor):
        # Test error handling for None input
        with pytest.raises(ValueError):
            zeno_processor.apply_zeno_stabilization(None)

    def test_apply_zeno_stabilization_with_empty_data(self, zeno_processor):
        with pytest.raises(ValueError):
            zeno_processor.apply_zeno_stabilization("")

    def test_stabilize_quantum_states_valid_data(self, zeno_processor, sample_sensor_fusion_data):
        result = zeno_processor._stabilize_quantum_states(sample_sensor_fusion_data)
        assert isinstance(result, SensorFusionData)

    def test_stabilize_quantum_states_invalid_type(self, zeno_processor):
        with pytest.raises(TypeError):
            zeno_processor._stabilize_quantum_states("invalid_data")

    def test_apply_zeno_effect(self, zeno_processor):
        stabilized_value = zeno_processor._apply_zeno_effect(1.5)
        expected_value = 1.5 * (1 - 0.01 * (1/100))
        assert abs(stabilized_value - expected_value) < 1e-10

    def test_normalize_value(self, zeno_processor):
        normalized = zeno_processor._normalize_value(5.0)
        assert normalized == 1.0  # 5.0/5.0 = 1.0

    def test_normalize_value_zero(self, zeno_processor):
        normalized = zeno_processor._normalize_value(0)
        assert normalized == 0

    def test_validate_and_normalize_data(self, zeno_processor, sample_sensor_fusion_data):
        result = zeno_processor._validate_and_normalize_data(sample_sensor_fusion_data)
        assert isinstance(result, SensorFusionData)

    def test_validate_and_normalize_data_invalid(self, zeno_processor):
        with pytest.raises(ValueError):
            zeno_processor._validate_and_normalize_data(None)

    def test_normalize_value_with_numpy(self, zeno_processor):
        # Test with different values
        test_values = [1.0, -2.5, 0.0, 10.0]
        for val in test_values:
            if val == 0:
                expected = 0
            else:
                expected = val / np.linalg.norm([val])
            result = zeno_processor._normalize_value(val)
            assert abs(result - expected) < 1e-10

    def test_apply_zeno_stabilization_with_multiple_readings(self, zeno_processor):
        readings = [
            SensorReading(sensor_id="sensor1", value=1.0, timestamp=datetime.now()),
            SensorReading(sensor_id="sensor2", value=2.0, timestamp=datetime.now()),
            SensorReading(sensor_id="sensor3", value=3.0, timestamp=datetime.now())
        ]
        fusion_data = SensorFusionData(
            sensor_readings=readings,
            fusion_timestamp=datetime.now()
        )
        
        result = zeno_processor.apply_zeno_stabilization(fusion_data)
        assert len(result.sensor_readings) == 3
        # Check that values have been stabilized
        for i, reading in enumerate(result.sensor_readings):
            expected_value = readings[i].value * (1 - 0.01 * (1/100))
            assert abs(reading.value - expected_value) < 1e-10

    def test_apply_zeno_stabilization_exception_handling(self, zeno_processor, sample_sensor_fusion_data):
        with patch.object(zeno_processor, '_stabilize_quantum_states', side_effect=Exception("Test exception")):
            with pytest.raises(Exception):
                zeno_processor.apply_zeno_stabilization(sample_sensor_fusion_data)

    def test_stabilize_quantum_states_exception_handling(self, zeno_processor, sample_sensor_fusion_data):
        with patch.object(zeno_processor, '_apply_zeno_effect', side_effect=Exception("Test exception")):
            with pytest.raises(Exception):
                zeno_processor._stabilize_quantum_states(sample_sensor_fusion_data)

    def test_apply_zeno_effect_exception_handling(self, zeno_processor):
        with patch.object(zeno_processor, '_normalize_value', side_effect=Exception("Test exception")):
            with pytest.raises(Exception):
                zeno_processor._validate_and_normalize_data(sample_sensor_fusion_data)

    def test_edge_case_empty_readings(self, zeno_processor):
        empty_data = SensorFusionData(
            sensor_readings=[],
            fusion_timestamp=datetime.now()
        )
        result = zeno_processor._stabilize_quantum_states(empty_data)
        assert result.sensor_readings == []

    def test_edge_case_large_values(self, zeno_processor):
        large_value = 1e10
        stabilized = zeno_processor._apply_zeno_effect(large_value)
        expected = large_value * (1 - 0.01 * (1/100))
        assert abs(stabilized - expected) < 1e-10

    def test_edge_case_negative_values(self, zeno_processor):
        negative_value = -5.0
        stabilized = zeno_processor._apply_zeno_effect(negative_value)
        expected = negative_value * (1 - 0.01 * (1/100))
        assert abs(stabilized - expected) < 1e-10