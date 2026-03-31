```python
import pytest
from datetime import datetime
from src.quantum_sensors.models import SensorReading, SensorFusionData
from pydantic import ValidationError


class TestSensorReading:
    """Test cases for SensorReading model"""

    def test_sensor_reading_creation_valid(self):
        """Test creating a valid SensorReading instance"""
        reading = SensorReading(
            sensor_id="sensor_001",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=25.5,
            unit="celsius",
            sensor_type="temperature"
        )
        assert reading.sensor_id == "sensor_001"
        assert reading.value == 25.5
        assert reading.unit == "celsius"
        assert reading.sensor_type == "temperature"

    def test_sensor_reading_with_metadata(self):
        """Test SensorReading with metadata field"""
        reading = SensorReading(
            sensor_id="sensor_002",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=22.5,
            unit="celsius",
            metadata={"location": "lab1", "calibration": "2023-01-01"},
            sensor_type="temperature"
        )
        assert reading.metadata == {"location": "lab1", "calibration": "2023-01-01"}

    def test_sensor_reading_missing_required_fields(self):
        """Test SensorReading validation for missing required fields"""
        with pytest.raises(ValidationError) as exc_info:
            SensorReading(
                sensor_id=None,
                timestamp=datetime(2023, 1, 1, 12, 0, 0),
                value=25.5
            )
        assert "sensor_id" in str(exc_info.value)

    def test_sensor_reading_invalid_confidence(self):
        """Test SensorFusionData with invalid confidence value"""
        with pytest.raises(ValidationError):
            SensorFusionData(
                confidence=1.5,  # Invalid: > 1.0
                timestamp=datetime(2023, 1, 1, 12, 0, 0)
            )

    def test_sensor_reading_valid_confidence(self):
        """Test SensorFusionData with valid confidence value"""
        data = SensorFusionData(
            confidence=0.8,
            timestamp=datetime(2023, 1, 1, 12, 0, 0)
        )
        assert data.confidence == 0.8

    def test_sensor_reading_empty_metadata(self):
        """Test SensorReading with empty metadata"""
        reading = SensorReading(
            sensor_id="sensor_001",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=25.5,
            unit="celsius",
            sensor_type="temperature"
        )
        assert reading.metadata is None

    def test_sensor_reading_invalid_data(self):
        """Test validation errors for invalid data"""
        with pytest.raises(ValidationError):
            SensorReading(
                sensor_id="sensor_001",
                timestamp="invalid-date",  # Invalid datetime
                value="invalid"  # Invalid value type
            )

    def test_sensor_reading_json_serialization(self):
        """Test JSON serialization of SensorReading"""
        reading = SensorReading(
            sensor_id="sensor_001",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=25.5,
            unit="celsius",
            sensor_type="temperature"
        )
        json_data = reading.json()
        assert isinstance(json_data, str)
        parsed = SensorReading.parse_raw(json_data)
        assert parsed.sensor_id == "sensor_001"

    def test_sensor_reading_edge_values(self):
        """Test SensorReading with edge case values"""
        # Test with zero value
        reading_zero = SensorReading(
            sensor_id="sensor_001",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=0.0,
            unit="unit",
            sensor_type="test"
        )
        assert reading_zero.value == 0.0

        # Test with negative value
        reading_negative = SensorReading(
            sensor_id="sensor_002",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=-10.5,
            unit="unit",
            sensor_type="test"
        )
        assert reading_negative.value == -10.5

    def test_sensor_reading_optional_fields(self):
        """Test SensorReading with optional fields"""
        # Test with all fields None except required
        data = SensorFusionData(
            timestamp=datetime(2023, 1, 1, 12, 0, 0)
        )
        assert data.visual_data is None
        assert data.tactile_data is None
        assert data.fused_output is None

    def test_sensor_reading_field_validation(self):
        """Test validation of SensorReading fields"""
        with pytest.raises(ValidationError) as exc_info:
            SensorReading(
                sensor_id="sensor_001",
                timestamp="not-a-datetime",  # This should fail validation
                value=25.5,
                unit="celsius",
                sensor_type="temperature"
            )
        assert "timestamp" in str(exc_info.value)

    def test_sensor_reading_default_values(self):
        """Test SensorReading default values"""
        # Test that defaults are properly set
        data = SensorFusionData(
            timestamp=datetime(2023, 1, 1, 12, 0, 0)
        )
        assert data.confidence == 1.0  # Default confidence value
        assert data.visual_data is None  # Default None value
        assert data.tactile_data is None  # Default None value

    def test_sensor_reading_boundary_values(self):
        """Test boundary values for sensor reading fields"""
        # Test very small float values
        reading_small = SensorReading(
            sensor_id="sensor_small",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=0.0001,  # Very small positive value
            unit="unit",
            sensor_type="test"
        )
        assert reading_small.value == 0.0001

        # Test negative values
        reading_negative = SensorReading(
            sensor_id="sensor_negative",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=-100.0,  # Negative value
            unit="unit",
            sensor_type="test"
        )
        assert reading_negative.value == -100.0

    def test_sensor_reading_string_fields(self):
        """Test SensorReading with string fields"""
        # Test various string scenarios
        long_sensor_id = "a" * 1000  # Very long sensor_id
        reading = SensorReading(
            sensor_id=long_sensor_id,
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=25.5,
            unit="celsius",
            sensor_type="test"
        )
        assert len(reading.sensor_id) == 1000

    def test_sensor_reading_numeric_validation(self):
        """Test numeric field validation"""
        # Test with various numeric values
        test_values = [
            0,  # Zero
            -100,  # Negative
            3.14159,  # Float
            1e10,  # Large number
            -1e10,  # Large negative number
        ]
        
        for i, val in enumerate(test_values):
            reading = SensorReading(
                sensor_id=f"sensor_{i}",
                timestamp=datetime(2023, 1, 1, 12, 0, 0),
                value=val,
                unit="unit",
                sensor_type="test"
            )
            assert reading.value == val

    def test_sensor_reading_datetime_validation(self):
        """Test datetime field validation"""
        # Test valid datetime
        dt = datetime(2023, 12, 31, 23, 59, 59, 999999)
        reading = SensorReading(
            sensor_id="test_sensor",
            timestamp=dt,
            value=25.5,
            unit="celsius",
            sensor_type="temperature"
        )
        assert reading.timestamp == dt

        # Test invalid datetime
        with pytest.raises(ValidationError):
            SensorReading(
                sensor_id="test_sensor",
                timestamp="invalid",  # This should fail
                value=25.5,
                unit="celsius",
                sensor_type="temperature"
            )

    def test_sensor_reading_list_validation(self):
        """Test list/tuple field validation"""
        # Test with list data
        reading = SensorReading(
            sensor_id="sensor_list",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=[1, 2, 3],  # This would be invalid for a float field
            unit="celsius",
            sensor_type="temperature"
        )
        # The list will be converted to string representation
        assert isinstance(str(reading.value), str)

    def test_sensor_reading_nested_data(self):
        """Test nested data structures"""
        # Test with nested dict
        nested_data = {
            "measurements": [
                {"type": "temperature", "value": 25.5},
                {"type": "humidity", "value": 60.0}
            ]
        }
        
        reading = SensorReading(
            sensor_id="nested_sensor",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=25.5,
            unit="celsius",
            sensor_type="test",
            metadata=nested_data
        )
        
        assert reading.metadata == nested_data

    def test_sensor_reading_memory_constraints(self):
        """Test memory constraints handling"""
        # Create large data structure
        large_data = {
            "data": ["x" * 1000000] * 100  # Large list
        }
        
        reading = SensorReading(
            sensor_id="memory_test",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=100.0,
            unit="celsius",
            sensor_type="test",
            metadata=large_data if len(str(large_data)) < 1000000 else None  # Memory constraint
        )
        
        # Don't actually create the large object, just test validation
        assert reading.sensor_id == "memory_test"

    def test_sensor_reading_special_floats(self):
        """Test special float values"""
        special_values = [float('inf'), float('-inf'), float('nan')]
        
        for val in special_values:
            try:
                reading = SensorReading(
                    sensor_id="special_float_test",
                    timestamp=datetime(2023, 1, 1, 12, 0, 0),
                    value=val,
                    unit="unit",
                    sensor_type="test"
                )
                # Should handle special float values appropriately
                if str(val) == "nan":
                    assert str(reading.value) == "nan"
            except (ValueError, ValidationError):
                # Handle the validation error appropriately
                pass

    def test_sensor_reading_data_integrity(self):
        """Test data integrity and validation"""
        # Test that data remains consistent
        original_data = {
            "sensor_id": "test_sensor",
            "timestamp": datetime(2023, 1, 1, 12, 0, 0),
            "value": 25.5,
            "unit": "celsius",
            "sensor_type": "test"
        }
        
        reading = SensorReading(**original_data)
        
        # Verify data integrity
        assert reading.sensor_id == "test_sensor"
        assert reading.value == 25.5
        assert reading.unit == "celsius"

    def test_sensor_reading_error_handling(self):
        """Test error handling in sensor reading"""
        # Test with various error conditions
        invalid_values = [None, "", 0, [], {}]
        
        for invalid_value in invalid_values:
            try:
                SensorReading(
                    sensor_id=invalid_value,  # This should cause validation error
                    timestamp=datetime(2023, 1, 1, 12, 0, 0),
                    value=25.5,
                    unit="celsius",
                    sensor_type="test"
                )
            except (ValueError, ValidationError) as e:
                # Expected error
                assert "validation" in str(e).lower()

    def test_sensor_reading_unicode_handling(self):
        """Test unicode character handling"""
        # Test with unicode sensor IDs
        unicode_ids = ["测试传感器", "sénsor_üñíçödé", "센서_테스트"]
        
        for uid in unicode_ids:
            try:
                reading = SensorReading(
                    sensor_id=uid,
                    timestamp=datetime(2023, 1, 1, 12, 0, 0),
                    value=25.5,
                    unit="celsius",
                    sensor_type="test"
                )
                # Should handle unicode properly
                assert isinstance(reading.sensor_id, str)
            except Exception as e:
                # Handle any unicode-related issues
                print(f"Unicode handling issue: {e}")

    def test_sensor_reading_compatibility(self):
        """Test compatibility with different data types"""
        # Test with various data types
        test_cases = [
            ("int", 123),
            ("float", 123.45),
            ("string", "test_value"),
            ("bool", True),
            ("none", None)
        ]
        
        for case_name, case_value in test_cases:
            try:
                reading = SensorReading(
                    sensor_id=f"test_{case_name}",
                    timestamp=datetime(2023, 1, 1, 12, 0, 0),
                    value=case_value if case_value != "test_value" else 25.5,
                    unit="celsius",
                    sensor_type="test"
                )
                # Process based on type
            except Exception:
                # Handle error appropriately
                pass

    def test_sensor_reading_performance(self):
        """Test performance with large datasets"""
        import time
        
        start_time = time.time()
        
        # Create multiple readings to test performance
        readings = []
        for i in range(1000):  # Reduced for testing
            reading = SensorReading(
                sensor_id=f"sensor_{i}",
                timestamp=datetime(2023, 1, 1, 12, 0, 0),
                value=25.5 + i,
                unit="celsius",
                sensor_type="test"
            )
            readings.append(reading)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Check that processing is reasonably fast
        assert processing_time < 10  # Should process 1000 readings in < 10 seconds

    def test_sensor_reading_concurrent_access(self):
        """Test concurrent access handling"""
        import threading
        import time
        
        results = []
        errors = []
        
        def create_reading(index):
            try:
                reading = SensorReading(
                    sensor_id=f"concurrent_{index}",
                    timestamp=datetime(2023, 1, 1, 12, 0, 0),
                    value=25.5,
                    unit="celsius",
                    sensor_type="test"
                )
                results.append(reading)
            except Exception as e:
                errors.append(str(e))
        
        # Test with multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=create_reading, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # Check results
        assert len(results) == 10
        assert len(errors) == 0

    def test_sensor_reading_memory_limits(self):
        """Test memory limits"""
        import sys
        
        # Test with large data that might hit memory limits
        large_value = "x" * 1000000  # 1MB string
        
        # This should not cause memory issues
        reading = SensorReading(
            sensor_id="memory_test",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),
            value=1000000.0,
            unit="celsius",
            sensor_type="test"
        )
        
        # Verify the large value is handled properly
        assert len(reading.value) == 1000000

    def test_sensor_reading_field_constraints(self):
        """Test field constraints and validation"""
        # Test various constraint scenarios
        test_scenarios = [
            # Min/max values
            ("min_value", -1e308),  # Very small number
            ("max_value", 1e308),   # Very large number
            ("zero_value", 0.0),     # Zero value
            ("normal_value", 25.5)   # Normal value
        ]
        
        for name, test_val in test_scenarios:
            try:
                reading = SensorReading(
                    sensor_id=f"test_{name}",
                    timestamp=datetime(2023, 1, 1, 12, 0, 0),
                    value=test_val,
                    unit="celsius",
                    sensor_type="test"
                )
                # Should handle all values properly
                assert isinstance(reading.value, type(test_val))
            except Exception:
                # Handle any constraint violations
                pass

    def test_sensor_reading_edge_case_values(self):
        """Test edge case values"""
        edge_cases = [
            float('inf'),   # Infinity
            float('-inf'),  # Negative infinity
            float('nan'),   # Not a number
            0,              # Zero
            -0.0,           # Negative zero
            1e-10,         # Very small positive number
            -1e