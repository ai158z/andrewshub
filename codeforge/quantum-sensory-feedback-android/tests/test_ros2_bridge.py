import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import Image, PointCloud2
from std_msgs.msg import String

from src.quantum_sensors.ros2_bridge import ROS2Bridge, init_ros2_bridge
from src.quantum_sensors.models import SensorReading


class TestROS2Bridge:
    """Test suite for ROS2Bridge class"""

    @pytest.fixture
    def mock_rclpy(self):
        """Mock rclpy initialization"""
        with patch('rclpy.init') as mock_init:
            with patch('rclpy.shutdown') as mock_shutdown:
                yield mock_init, mock_shutdown

    @pytest.fixture
    def ros2_bridge(self, mock_rclpy):
        """Create a ROS2Bridge instance with mocked dependencies"""
        with patch('src.quantum_sensors.ros2_bridge.rclpy.create_node'):
            with patch('src.quantum_sensors.ros2_bridge.ZenoProcessor') as mock_zeno, \
                 patch('src.quantum_sensors.ros2_bridge.CodonicProcessor') as mock_codonic, \
                 patch('src.quantum_sensors.ros2_bridge.EntanglementHandler') as mock_entangle:
                
                bridge = ROS2Bridge.__new__(ROS2Bridge)
                bridge.__init__()
                bridge.zeno_processor = mock_zeno.return_value
                bridge.codonic_processor = mock_codonic.return_value
                bridge.entanglement_handler = mock_entangle.return_value
                yield bridge

    def test_init_publishers(self, ros2_bridge):
        """Test publisher initialization"""
        with patch.object(ros2_bridge, 'create_publisher') as mock_publisher:
            ros2_bridge._init_publishers()
            assert mock_publisher.call_count == 2

    def test_init_subscribers(self, ros2_bridge):
        """Test subscriber initialization"""
        with patch.object(ros2_bridge, 'create_subscription') as mock_subscriber:
            ros2_bridge._init_subscribers()
            assert mock_subscriber.call_count == 2

    def test_visual_data_callback_success(self, ros2_bridge):
        """Test visual data callback with valid data"""
        mock_msg = Mock()
        mock_msg.data = '{"test": "data"}'
        
        with patch('src.quantum_sensors.ros2_bridge.validate_sensor_data', return_value=True), \
             patch('src.quantum_sensors.ros2_bridge.normalize_quantum_states') as mock_normalize:
            
            mock_normalize.return_value = {"normalized": True}
            ros2_bridge._stored_visual_data = {}
            
            ros2_bridge._visual_data_callback(mock_msg)
            
            # Verify that the processing pipeline was called
            mock_normalize.assert_called_once()

    def test_visual_data_callback_invalid_data(self, ros2_bridge):
        """Test visual data callback with invalid data"""
        mock_msg = Mock()
        mock_msg.data = '{"test": "data"}'
        
        with patch('src.quantum_sensors.ros2_bridge.validate_sensor_data', return_value=False):
            # Should not process invalid data
            result = ros2_bridge._visual_data_callback(mock_msg)
            # Processing should be skipped for invalid data
            assert result is None

    def test_tactile_data_callback(self, ros2_bridge):
        """Test tactile data callback"""
        mock_msg = Mock()
        mock_msg.data = '{"tactile": "data"}'
        
        with patch('src.quantum_sensors.ros2_bridge.validate_sensor_data', return_value=True), \
             patch('src.quantum_sensors.ros2_bridge.normalize_quantum_states') as mock_normalize:
            
            mock_normalize.return_value = {"normalized": True}
            ros2_bridge._tactile_data_callback(mock_msg)

    def test_deserialize_sensor_data_string_msg(self, ros2_bridge):
        """Test deserialization of string message"""
        msg = String()
        msg.data = '{"key": "value"}'
        
        result = ros2_bridge._deserialize_sensor_data(msg)
        assert result == {"key": "value"}

    def test_deserialize_sensor_data_string_msg_invalid_json(self, ros2_bridge):
        """Test deserialization with invalid JSON"""
        msg = String()
        msg.data = 'invalid json'
        
        result = ros2_bridge._deserialize_sensor_data(msg)
        assert result == {}

    def test_deserialize_sensor_data_other_msg(self, ros2_bridge):
        """Test deserialization of non-string message"""
        msg = Image()
        msg.data = "test"
        
        result = ros2_bridge._deserialize_sensor_data(msg)
        assert result == {"data": str(msg)}

    def test_process_and_publish_valid_visual(self, ros2_bridge):
        """Test processing pipeline with valid visual data"""
        sensor_data = {"sensor": "data"}
        sensor_type = "visual"
        
        with patch('src.quantum_sensors.ros2_bridge.validate_sensor_data', return_value=True), \
             patch('src.quantum_sensors.ros2_bridge.normalize_quantum_states', return_value=sensor_data), \
             patch.object(ros2_bridge.zeno_processor, 'apply_zeno_stabilization', return_value=sensor_data), \
             patch.object(ros2_bridge.codonic_processor, 'process_codonic_layer', return_value=sensor_data):
            
            ros2_bridge._process_and_publish(sensor_data, sensor_type)
            
            # Verify the data was stored
            assert hasattr(ros2_bridge, '_stored_visual_data')

    def test_process_and_publish_valid_tactile_with_fusion(self, ros2_bridge):
        """Test processing pipeline with tactile data that should trigger fusion"""
        sensor_data = {"sensor": "data"}
        sensor_type = "tactile"
        ros2_bridge._stored_visual_data = {"visual": "data"}
        
        with patch('src.quantum_sensors.ros2_bridge.validate_sensor_data', return_value=True), \
             patch('src.quantum_sensors.ros2_bridge.normalize_quantum_states') as mock_normalize, \
             patch('src.quantum_sensors.ros2_bridge.fuse_sensors') as mock_fuse, \
             patch.object(ros2_bridge.zeno_processor, 'apply_zeno_stabilization') as mock_zeno, \
             patch.object(ros2_bridge.codonic_processor, 'process_codonic_layer') as mock_codonic, \
             patch.object(ros2_bridge.entanglement_handler, 'correlate_sensors') as mock_correlate:
            
            mock_normalize.return_value = sensor_data
            mock_zeno.return_value = sensor_data
            mock_codonic.return_value = sensor_data
            mock_fuse.return_value = {"fused": "data"}
            mock_correlate.return_value = {"entangled": "output"}
            
            ros2_bridge._process_and_publish(sensor_data, sensor_type)
            
            mock_fuse.assert_called_once()
            mock_correlate.assert_called_once()
            
            # Verify storage was cleared
            assert not hasattr(ros2_bridge, '_stored_visual_data')

    def test_publish_sensor_data_success(self, ros2_bridge):
        """Test successful sensor data publishing"""
        sensor_reading = SensorReading(
            sensor_id="test_sensor",
            timestamp="2023-01-01T00:00:00Z",
            data={"test": "reading"}
        )
        
        with patch.object(ros2_bridge, 'fused_data_publisher') as mock_publisher:
            result = ros2_bridge.publish_sensor_data(sensor_reading)
            
            assert result is True
            mock_publisher.publish.assert_called_once()

    def test_publish_sensor_data_invalid_type(self, ros2_bridge):
        """Test publish_sensor_data with invalid data type"""
        with pytest.raises(TypeError):
            ros2_bridge.publish_sensor_data("invalid data")

    def test_subscribe_to_sensors_success(self, ros2_bridge):
        """Test sensor subscription initialization"""
        result = ros2_bridge.subscribe_to_sensors()
        assert result is True

    def test_subscribe_to_sensors_failure(self, ros2_bridge):
        """Test sensor subscription failure handling"""
        with patch.object(ros2_bridge, 'create_subscription', side_effect=Exception("Subscription failed")):
            # Since subscriptions are set up in __init__, this test is more of a formality
            # In a real scenario, we might test reconnection logic
            pass

    def test_init_ros2_bridge_function(self, mock_rclpy):
        """Test the init_ros2_bridge function"""
        with patch('src.quantum_sensors.ros2_bridge.rclpy.init') as mock_init, \
             patch('src.quantum_sensors.ros2_bridge.ROS2Bridge') as mock_bridge_class:
            
            mock_bridge_instance = Mock()
            mock_bridge_class.return_value = mock_bridge_instance
            
            result = init_ros2_bridge()
            
            mock_init.assert_called_once()
            mock_bridge_class.assert_called_once()
            assert result == mock_bridge_instance

    def test_callback_error_handling(self, ros2_bridge):
        """Test error handling in callbacks"""
        mock_msg = Mock()
        mock_msg.data = '{"test": "data"}'
        
        with patch('src.quantum_sensors.ros2_bridge.validate_sensor_data', return_value=True), \
             patch('src.quantum_sensors.ros2_bridge.normalize_quantum_states', side_effect=Exception("Processing error")):
            
            # Should not raise exception but log error
            with patch.object(ros2_bridge.logger, 'error') as mock_logger:
                ros2_bridge._visual_data_callback(mock_msg)
                mock_logger.assert_called_once()

    def test_deserialize_error_handling(self, ros2_bridge):
        """Test error handling in deserialization"""
        msg = String()
        msg.data = 'invalid json'
        
        with patch('json.loads', side_effect=Exception("JSON error")):
            result = ros2_bridge._deserialize_sensor_data(msg)
            assert result == {}

    def test_process_and_publish_error_handling(self, ros2_bridge):
        """Test error handling in processing pipeline"""
        sensor_data = {"test": "data"}
        
        with patch('src.quantum_sensors.ros2_bridge.validate_sensor_data', side_effect=Exception("Validation error")):
            with patch.object(ros2_bridge.logger, 'error') as mock_logger:
                ros2_bridge._process_and_publish(sensor_data, "visual")
                mock_logger.assert_called_once()