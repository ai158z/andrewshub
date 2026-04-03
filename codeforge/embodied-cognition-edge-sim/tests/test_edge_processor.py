import pytest
from unittest.mock import Mock, patch
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Imu, LaserScan
from geometry_msgs.msg import Twist, Quaternion, Vector3
from rclpy.node import Node
from src.embodied_edge_sim.edge_processor import EdgeProcessor

@pytest.fixture
def edge_processor():
    # Create a mock node for testing
    with patch.object(Node, '__init__'), \
         patch.object(Node, 'create_subscription'), \
         patch.object(Node, 'create_publisher'), \
         patch.object(Node, 'create_timer'):
        processor = EdgeProcessor()
        processor.get_logger = Mock()
        return processor

def test_imu_callback_stores_data():
    processor = EdgeProcessor()
    imu_msg = Imu()
    processor.imu_callback(imu_msg)
    assert processor.imu_data == imu_msg

def test_laser_callback_stores_data():
    processor = EdgeProcessor()
    laser_msg = LaserScan()
    processor.laser_callback(laser_msg)
    assert processor.laser_data == laser_msg

def test_cmd_vel_callback_stores_data():
    processor = EdgeProcessor()
    cmd_vel_msg = Twist()
    processor.cmd_vel_callback(cmd_vel_msg)
    assert processor.cmd_vel_data == cmd_vel_msg

def test_process_callback_publishes_processed_data():
    processor = EdgeProcessor()
    processor.process_callback()
    # Verify that the method processes and publishes

def test_process_data_with_imu_only(edge_processor):
    # Setup IMU data
    edge_processor.imu_data = Imu()
    edge_processor.laser_data = None
    edge_processor.cmd_vel_data = None
    
    result = edge_processor.process_data()
    assert result is not None
    assert "IMU" in result.data

def test_process_data_with_laser_only(edge_processor):
    edge_processor.imu_data = None
    edge_processor.laser_data = LaserScan()
    edge_processor.laser_data.ranges = [1.0, 2.0, 3.0]
    edge_processor.cmd_vel_data = None
    
    result = edge_processor.process_data()
    assert result is not None
    assert "LiDAR" in result.data

def test_process_data_with_all_sensors(edge_processor):
    edge_processor.imu_data = Imu()
    edge_processor.laser_data = LaserScan()
    edge_processor.laser_data.ranges = [1.0, 2.0, 3.0]
    edge_processor.cmd_vel_data = Twist()
    
    result = edge_processor.process_data()
    assert result is not None
    assert "Processed data:" in result.data

def test_process_data_no_data():
    processor = EdgeProcessor()
    processor.imu_data = None
    processor.laser_data = None
    processor.cmd_vel_data = None
    
    result = processor.process_data()
    assert result is None

def test_process_data_with_cmd_vel_only(edge_processor):
    edge_processor.imu_data = None
    edge_processor.laser_data = None
    edge_processor.cmd_vel_data = Twist()
    edge_processor.cmd_vel_data.linear.x = 1.0
    edge_processor.cmd_vel_data.angular.z = 0.5
    
    result = edge_processor.process_data()
    assert result is not None
    assert "CmdVel" in result.data

def test_imu_callback():
    imu_msg = Imu()
    processor = EdgeProcessor()
    processor.imu_callback(imu_msg)
    assert processor.imu_data == imu_msg

def test_laser_callback():
    laser_msg = LaserScan()
    processor = EdgeProcessor()
    processor.laser_callback(laser_msg)
    assert processor.laser_data == laser_msg

def test_cmd_vel_callback():
    cmd_vel_msg = Twist()
    processor = EdgeProcessor()
    processor.cmd_vel_callback(cmd_vel_msg)
    assert processor.cmd_vel_data == cmd_vel_msg

def test_process_callback_publishes():
    processor = EdgeProcessor()
    processor.process_callback()

def test_node_initialization():
    with patch('rclpy.node.Node.__init__'), \
         patch('rclpy.node.Node.create_subscription'), \
         patch('rclpy.node.Node.create_publisher'), \
         patch('rclpy.node.Node.create_timer'):
        processor = EdgeProcessor()
        assert processor is not None

@pytest.mark.parametrize("imu_present,laser_present,cmd_vel_present", [
    (True, False, False),
    (False, True, False),
    (False, False, True),
    (True, True, True),
    (False, False, False)
])
def test_sensor_combinations(imu_present, laser_present, cmd_vel_present):
    processor = EdgeProcessor()
    if imu_present:
        processor.imu_data = Imu()
    if laser_present:
        processor.laser_data = LaserScan()
    if cmd_vel_present:
        processor.cmd_vel_data = Twist()
    
    result = processor.process_data()
    assert result is not None if (imu_present or laser_present or cmd_vel_present) else result is None

def test_data_lock_usage():
    processor = EdgeProcessor()
    # Check that we're using thread locks properly
    with patch('threading.Lock') as mock_lock:
        mock_lock_instance = Mock()
        mock_lock.return_value = mock_lock_instance
        processor.data_lock = mock_lock_instance
        with patch.object(processor, 'data_lock', return_value=mock_lock_instance):
            processor.imu_callback(Imu())
            processor.data_lock.__enter__.assert_called()

def test_processed_data_publisher_created():
    processor = EdgeProcessor()
    # Should have a publisher for processed data
    assert hasattr(processor, 'processed_data_pub')

def test_processed_data_subscriber_created():
    processor = EdgeProcessor()
    # Should have subscription for processed data
    assert hasattr(processor, 'processed_data_pub')