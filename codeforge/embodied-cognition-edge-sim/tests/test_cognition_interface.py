import pytest
from unittest.mock import Mock, patch, MagicMock
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_msgs.msg import String
import numpy as np

from src.embodied_edge_sim.cognition_interface import CognitionInterface

@pytest.fixture
def cognition_interface():
    with patch('rclpy.node.Node.__init__', lambda self, name: None):
        with patch('rclpy.node.Node.create_subscription'):
            with patch('rclpy.node.Node.create_publisher'):
                interface = CognitionInterface()
                interface.get_clock = Mock(return_value=Mock())
                interface.get_clock.return_value.now.return_value = Mock()
                interface.get_clock.return_value.now.return_value.to_msg.return_value = "timestamp"
                return interface

def test_sensor_data_callback_success(cognition_interface):
    # Setup
    msg = String()
    msg.data = "test_data"
    
    # Mock all dependencies
    cognition_interface.edge_processor.process_data = Mock(return_value="processed")
    cognition_interface.latency_model.get_latency = Mock(return_value=0.1)
    cognition_interface.latency_model.apply_latency = Mock(return_value="processed_with_latency")
    cognition_interface.data_visualizer.visualize_flow = Mock()
    
    # Execute
    cognition_interface.sensor_data_callback(msg)
    
    # Verify
    cognition_interface.edge_processor.process_data.assert_called_once_with("test_data")
    cognition_interface.latency_model.get_latency.assert_called_once()
    cognition_interface.data_visualizer.visualize_flow.assert_called_once_with("processed_with_latency")

def test_sensor_data_callback_exception_handling(cognition_interface):
    # Setup
    msg = String()
    msg.data = "test_data"
    cognition_interface.edge_processor.process_data = Mock(side_effect=Exception("Processing error"))
    
    # Execute
    cognition_interface.sensor_data_callback(msg)
    
    # Verify that exception is handled and logged

def test_odom_callback_success(cognition_interface):
    # Setup
    msg = Odometry()
    msg.pose = Mock()
    msg.pose.pose = "test_pose"
    
    # Execute
    cognition_interface.odom_callback(msg)
    
    # Verify
    assert cognition_interface.current_pose == "test_pose"

def test_odom_callback_exception_handling(cognition_interface):
    # Setup
    msg = Odometry()
    msg.pose = Mock()
    msg.pose.pose = "test_pose"
    cognition_interface.current_pose = None
    
    with patch.object(cognition_interface, 'odom_callback', side_effect=Exception):
        pass
    
    # Execute
    # Just verify it doesn't crash

def test_make_decision_with_history(cognition_interface):
    # Setup
    cognition_interface.decision_history = [{"test": "data"}]
    cognition_interface.get_clock().now().to_msg.return_value = "timestamp"
    
    # Execute
    cmd = cognition_interface.make_decision()
    
    # Verify
    assert isinstance(cmd, Twist)
    assert cmd.linear.x == 0.5
    assert cmd.angular.z == 0.0

def test_make_decision_no_history(cognition_interface):
    # Setup
    cognition_interface.decision_history = []
    
    # Execute
    result = cognition_interface.make_decision()
    
    # Verify
    assert result is None

def test_make_decision_empty_history(cognition_interface):
    # Setup
    cognition_interface.decision_history = []
    
    # Execute
    result = cognition_interface.make_decision()
    
    # Verify
    assert result is None

def test_make_decision_exception_handling(cognition_interface):
    # Setup
    cognition_interface.decision_history = [{}]
    cognition_interface.get_clock = Mock(side_effect=Exception("Test exception"))
    
    # Execute
    result = cognition_interface.make_decision()
    
    # Verify
    assert result is None

def test_execute_action_success(cognition_interface):
    # Setup
    cmd = Twist()
    cmd.linear.x = 1.0
    cmd.angular.z = 0.5
    
    # Mock publisher
    cognition_interface.cmd_vel_publisher.publish = Mock()
    
    # Execute
    cognition_interface.execute_action(cmd)
    
    # Verify
    cognition_interface.cmd_vel_publisher.publish.assert_called_once_with(cmd)

def test_execute_action_none(cognition_interface):
    # Execute
    cognition_interface.execute_action(None)
    
    # Verify that it doesn't crash

def test_execute_action_exception_handling(cognition_interface):
    # Setup
    cmd = Twist()
    cmd.linear.x = 1.0
    cognition_interface.cmd_vel_publisher.publish = Mock(side_effect=Exception("Publish error"))
    
    # Execute
    cognition_interface.execute_action(cmd)
    
    # Verify that exception is handled

def test_publish_scan_success(cognition_interface):
    # Setup
    scan_data = LaserScan()
    
    # Mock publisher
    cognition_interface.scan_publisher.publish = Mock()
    
    # Execute
    cognition_interface.publish_scan(scan_data)
    
    # Verify
    cognition_interface.scan_publisher.publish.assert_called_once_with(scan_data)
    assert cognition_interface.current_scan == scan_data

def test_publish_scan_exception_handling(cognition_interface):
    # Setup
    scan_data = LaserScan()
    cognition_interface.scan_publisher.publish = Mock(side_effect=Exception("Publish error"))
    
    # Execute
    cognition_interface.publish_scan(scan_data)
    
    # Verify that exception is handled

def test_get_current_state(cognition_interface):
    # Setup
    cognition_interface.current_pose = "test_pose"
    cognition_interface.current_scan = "test_scan"
    cognition_interface.decision_history = [{"test": "history"}]
    
    # Execute
    state = cognition_interface.get_current_state()
    
    # Verify
    assert state['current_pose'] == "test_pose"
    assert state['current_scan'] == "test_scan"
    assert state['decision_history'] == [{"test": "history"}]

def test_initialization(cognition_interface):
    # Verify components are initialized
    assert cognition_interface.edge_processor is not None
    assert cognition_interface.latency_model is not None
    assert cognition_interface.data_visualizer is not None
    assert cognition_interface.callback_group is not None

@patch('rclpy.node.Node.create_subscription')
@patch('rclpy.node.Node.create_publisher')
def test_node_subscriptions_and_publishers(mock_create_publisher, mock_create_subscription):
    # Execute
    cognition_interface = CognitionInterface("test_node")
    
    # Verify subscriptions and publishers were created
    assert mock_create_subscription.call_count == 2  # Two subscribers created
    assert mock_create_publisher.call_count == 2  # Two publishers created

def test_cleanup(cognition_interface):
    # Setup
    cognition_interface.destroy_node = Mock()
    
    # Execute
    cognition_interface.cleanup()
    
    # Verify
    cognition_interface.destroy_node.assert_called_once()

def test_main_function():
    with patch('rclpy.init') as mock_init:
        with patch('rclpy.shutdown') as mock_shutdown:
            with patch('rclpy.node.Node.__init__', lambda self, name: None):
                with patch('rclpy.node.Node.create_subscription'):
                    with patch('rclpy.node.Node.create_publisher'):
                        with patch('rclpy.executors.SingleThreadedExecutor') as mock_executor:
                            # Execute
                            from src.embodied_edge_sim.cognition_interface import main
                            main()
                            
                            # Verify
                            mock_init.assert_called_once()
                            mock_shutdown.assert_called_once()

def test_callback_group_initialization(cognition_interface):
    # Verify callback group is properly initialized
    assert cognition_interface.callback_group is not None

def test_logger_initialization(cognition_interface):
    # Verify logger is properly initialized
    assert cognition_interface.logger is not None