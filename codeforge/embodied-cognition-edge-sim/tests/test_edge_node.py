import pytest
import rclpy
from rclpy.node import Node
from unittest.mock import patch, MagicMock
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan, Odometry
from geometry_msgs.msg import Twist
import time
import json

# Import the module to test
from src.embodied_edge_sim.edge_node import EdgeNode

@pytest.fixture
def edge_node():
    rclpy.init(args=None)
    node = EdgeNode()
    return node

def test_edge_node_initialization(edge_node):
    assert edge_node.node_state == "ACTIVE"
    assert hasattr(edge_node, 'decision_publisher')
    assert hasattr(edge_node, 'status_publisher')

def test_edge_node_scan_callback_publishes_status(edge_node):
    # Setup
    msg = LaserScan()
    msg.header.stamp.sec = int(time.time())
    msg.header.stamp.nanosec = 0
    
    # Test
    with patch.object(edge_node.status_publisher, 'publish') as mock_publish:
        edge_node.scan_callback(msg)
        mock_publish.assert_called()

def test_edge_node_odom_callback_publishes_status(edge_node):
    # Setup
    msg = Odometry()
    msg.header.stamp.sec = int(time.time())
    msg.header.stamp.nanosec = 0
    
    # Test
    with patch.object(edge_node.status_publisher, 'publish') as mock_publish:
        edge_node.odom_callback(msg)
        mock_publish.assert_called()

def test_edge_node_scan_callback_stores_data(edge_node):
    # Setup
    msg = LaserScan()
    msg.header.stamp.sec = int(time.time())
    msg.header.stamp.nanosec = 0
    
    # Test
    with patch.object(edge_node.edge_processor, 'process_data') as mock_process:
        mock_process.return_value = {'test': 'data'}
        edge_node.scan_callback(msg)
        mock_process.assert_called()

def test_edge_node_odom_callback_stores_data(edge_node):
    # Setup
    msg = Odometry()
    msg.header.stamp.sec = int(time.time())
    msg.header.stamp.nanosec = 0
    
    # Test
    with patch.object(edge_node.edge_processor, 'process_data') as mock_process:
        mock_process.return_value = {'test': 'data'}
        edge_node.odom_callback(msg)
        mock_process.assert_called()

def test_edge_node_processing_timer_callback_no_data(edge_node):
    edge_node.local_data = {}
    
    # Test
    with patch.object(edge_node.decision_publisher, 'publish') as mock_publish:
        edge_node.processing_timer_callback()
        mock_publish.assert_not_called()

def test_edge_node_processing_timer_callback_with_data(edge_node):
    edge_node.local_data = {'scan': [1, 2, 3]}
    
    # Test
    with patch.object(edge_node.edge_processor, 'process_data') as mock_process:
        mock_process.return_value = {'processed': 'data'}
        with patch.object(edge_node.decision_publisher, 'publish') as mock_publish:
            edge_node.processing_timer_callback()
            mock_publish.assert_called()

def test_edge_node_destroy_node(edge_node):
    with patch.object(edge_node, 'get_logger') as mock_logger:
        edge_node.destroy_node()
        mock_logger.return_value.info.assert_called()

def test_edge_node_scan_callback_error_handling(edge_node):
    # Setup
    msg = LaserScan()
    
    # Test
    with patch.object(edge_node.latency_model, 'get_latency', return_value=0.1):
        with patch.object(edge_node.latency_model, 'apply_latency', return_value=msg):
            with patch.object(edge_node.edge_processor, 'process_data', return_value={}):
                with patch.object(edge_node.status_publisher, 'publish'):
                    edge_node.scan_callback(msg)
                    
                    # Verify that error handling works
                    edge_node.get_logger().error.assert_not_called()

def test_edge_node_odom_callback_error_handling(edge_node):
    # Setup
    msg = Odometry()
    
    # Test
    with patch.object(edge_node.latency_model, 'get_latency', return_value=0.1):
        with patch.object(edge_node.latency_model, 'apply_latency', return_value=msg):
            with patch.object(edge_node.edge_processor, 'process_data', return_value={}):
                with patch.object(edge_node.status_publisher, 'publish'):
                    edge_node.odom_callback(msg)
                    
                    # Verify that error handling works
                    edge_node.get_logger().error.assert_not_called()

def test_edge_node_main_function():
    with patch('rclpy.init') as mock_init:
        with patch('rclpy.shutdown') as mock_shutdown:
            with patch('rclpy.create_node', return_value=MagicMock()):
                # Test
                from src.embodied_edge_sim.edge_node import main
                main()
                mock_init.assert_called()
                mock_shutdown.assert_called()

def test_edge_node_main_keyboard_interrupt():
    with patch('rclpy.init') as mock_init:
        with patch('rclpy.shutdown') as mock_shutdown:
            with patch('rclpy.create_node', return_value=MagicMock()):
                with patch('builtins.input', return_value=KeyboardInterrupt):
                    # Test
                    try:
                        from src.embodied_edge_sim.edge_node import main
                        main()
                    except KeyboardInterrupt:
                        pass
                    mock_init.assert_called()
                    mock_shutdown.assert_called()

def test_edge_node_main_exception():
    with patch('rclpy.init') as mock_init:
        with patch('rclpy.shutdown') as mock_shutdown:
            with patch('rclpy.create_node', return_value=MagicMock()):
                with patch('builtins.input', side_effect=Exception("Test exception")):
                    # Test
                    try:
                        from src.embodied_edge_sim.edge_node import main
                        main()
                    except Exception:
                        pass
                    mock_init.assert_called()
                    mock_shutdown.assert_called()

def test_edge_node_parameters_declared(edge_node):
    assert edge_node.node_id is not None
    assert edge_node.simulation_mode is not None
    assert edge_node.processing_rate is not None

def test_edge_node_callback_groups_created(edge_node):
    assert edge_node.callback_group is not None

def test_edge_node_publishers_created(edge_node):
    assert edge_node.decision_publisher is not None
    assert edge_node.status_publisher is not None
    assert edge_node.scan_subscription is not None
    assert edge_node.odom_subscription is not None

def test_edge_node_timers_created(edge_node):
    assert edge_node.timer is not None

def test_edge_node_scan_callback_with_latency(edge_node):
    # Setup
    msg = LaserScan()
    msg.header.stamp.sec = int(time.time())
    msg.header.stamp.nanosec = 0
    
    # Test
    with patch.object(edge_node.latency_model, 'get_latency', return_value=0.1):
        with patch.object(edge_node.latency_model, 'apply_latency', return_value=msg):
            with patch.object(edge_node.edge_processor, 'process_data', return_value={'processed': True}):
                with patch.object(edge_node.status_publisher, 'publish') as mock_publish:
                    edge_node.scan_callback(msg)
                    mock_publish.assert_called()

def test_edge_node_odom_callback_with_latency(edge_node):
    # Setup
    msg = Odometry()
    msg.header.stamp.sec = int(time.time())
    msg.header.stamp.nanosec = 0
    
    # Test
    with patch.object(edge0.odom_callback, 'get_latency', return_value=0.1):
        with patch.object(edge_node.latency_model, 'apply_latency', return_value=msg):
            with patch.object(edge_node.status_publisher, 'publish') as mock_publish:
                edge_node.odom_callback(msg)
                mock_publish.assert_called()

def test_edge_node_processing_callback_with_data(edge_node):
    edge_node.local_data = {'scan': [1, 2, 3]}
    
    # Test
    with patch.object(edge_node.edge_processor, 'process_data', return_value={'processed': True}):
        with patch.object(edge_node.decision_publisher, 'publish') as mock_publish:
            edge_node.processing_timer_callback()
            mock_publish.assert_called()

def test_edge_node_processing_callback_without_data(edge_node):
    edge_node.local_data = {}
    
    # Test
    with patch.object(edge_node.decision_publisher, 'publish') as mock_publish:
        edge_node.processing_timer_callback()
        mock_publish.assert_not_called()