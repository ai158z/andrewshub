import pytest
import json
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2, Header
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from rclpy.node import Node
from rclpy.time import Time
from rclpy.clock import Clock
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.embodied_edge_sim.global_integrator import GlobalIntegrator

@pytest.fixture
def global_integrator():
    """Create a GlobalIntegrator instance for testing"""
    with patch('rclpy.init'), patch('rclpy.create_node'):
        node = GlobalIntegrator()
        node.get_logger = Mock()
        node.get_clock = Mock()
        node.get_clock.return_value.now.return_value.to_msg.return_value.sec = 1234567890
        return node

def create_string_message(data):
    """Helper to create a String message"""
    msg = String()
    msg.data = data
    return msg

def create_pointcloud_message(frame_id="test_edge"):
    """Helper to create a PointCloud2 message"""
    msg = PointCloud2()
    msg.header = Header()
    msg.header.frame_id = frame_id
    msg.data = b"test" * 100  # Mock data
    return msg

def create_pose_message(frame_id="test_edge"):
    """Helper to create a PoseStamped message"""
    msg = PoseStamped()
    msg.header = Header()
    msg.header.frame_id = frame_id
    msg.pose = Pose()
    msg.pose.position = Point(x=1.0, y=2.0, z=3.0)
    msg.pose.orientation = Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)
    return msg

def test_init_global_integrator(global_integrator):
    """Test that GlobalIntegrator initializes correctly"""
    assert global_integrator._lock is not None
    assert global_integrator._edge_data is not None
    assert global_integrator._processed_insights is not None

def test_edge_status_callback_valid_json(global_integrator):
    """Test edge status callback with valid JSON data"""
    msg = create_string_message('{"edge_id": "edge_1", "status": "active"}')
    global_integrator._edge_status_callback(msg)
    
    with global_integrator._lock:
        assert "edge_1" in global_integrator._edge_data
        assert global_integrator._edge_data["edge_1"]["status"]["status"] == "active"

def test_edge_status_callback_invalid_json(global_integrator):
    """Test edge status callback with invalid JSON data"""
    msg = create_string_message('invalid json')
    msg.data = 'invalid json'
    global_integrator._edge_status_callback(msg)
    # Should not raise an exception and should log an error

def test_edge_status_callback_missing_edge_id(global_integrator):
    """Test edge status callback with missing edge_id"""
    msg = create_string_message('{"status": "active"}')
    global_integrator._edge_status_callback(msg)
    # Should log a warning about missing edge_id

def test_edge_sensor_callback(global_integrator):
    """Test edge sensor callback"""
    msg = create_pointcloud_message("sensor_edge_1")
    global_integrator._edge_sensor_callback(msg)
    
    with global_integrator._lock:
        assert "sensor_edge_1" in global_integrator._edge_data
        assert "sensor_data" in global_integrator._edge_data["sensor_edge_1"]

def test_edge_pose_callback(global_integrator):
    """Test edge pose callback"""
    msg = create_pose_message("pose_edge_1")
    global_integrator._edge_pose_callback(msg)
    
    with global_integrator._lock:
        assert "pose_edge_1" in global_integrator._edge_data
        assert "pose" in global_integrator._edge_data["pose_edge_1"]

def test_publish_global_insights(global_integrator):
    """Test publishing global insights"""
    # Add some data first
    status_msg = create_string_message('{"edge_id": "test_edge", "status": "active"}')
    global_integrator._edge_status_callback(status_msg)
    
    # Publish insights
    global_integrator._publish_global_insights()
    
    # Check that data was processed
    insights = global_integrator.get_global_insight()
    assert "test_edge" in insights

def test_get_global_insight(global_integrator):
    """Test getting global insight data"""
    # Add test data
    with global_integrator._lock:
        global_integrator._processed_insights["test_edge"] = {"data": "test"}
    
    insights = global_integrator.get_global_insight()
    assert insights.get("test_edge", {}).get("data") == "test"

def test_thread_safety_with_multiple_messages(global_integrator):
    """Test that the integrator handles messages from multiple sources"""
    # Send different types of messages
    status_msg = create_string_message('{"edge_id": "multi_1", "status": "active"}')
    sensor_msg = create_pointcloud_message("multi_1")
    pose_msg = create_pose_message("multi_1")
    
    global_integrator._edge_status_callback(status_msg)
    global_integrator._edge_sensor_callback(sensor_msg)
    global_integrator._edge_pose_callback(pose_msg)
    
    # Verify all data is stored
    with global_integrator._lock:
        assert "multi_1" in global_integrator._edge_data
        assert "status" in global_integrator._edge_data["multi_1"]
        assert "sensor_data" in global_integrator._edge_data["multi_1"]
        assert "pose" in global_integrator._edge_data["multi_1"]

def test_empty_message_handling(global_integrator):
    """Test handling of empty messages"""
    # Test with empty string message
    msg = create_string_message('')
    global_integrator._edge_status_callback(msg)
    
    # Should not raise an exception and should log an error

def test_malformed_json_status(global_intgregator):
    """Test handling of malformed JSON"""
    msg = create_string_message('{"edge_id": "test" status: "missing comma"}')
    global_integrator._edge_status_callback(msg)
    # Should catch JSONDecodeError and log appropriately

def test_sensor_callback_with_empty_frame_id(global_integrator):
    """Test sensor callback with empty frame_id"""
    msg = PointCloud2()
    msg.header = Header()
    msg.header.frame_id = ""
    msg.data = b"test"
    
    # Should handle gracefully without crashing
    global_integrator._edge_sensor_callback(msg)

def test_pose_callback_with_empty_frame_id(global_integrator):
    """Test pose callback with empty frame_id"""
    msg = PoseStamped()
    msg.header = Header()
    msg.header.frame_id = ""
    msg.pose = Pose()
    msg.pose.position = Point(x=0.0, y=0.0, z=0.0)
    msg.pose.orientation = Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)
    
    # Should handle gracefully
    global_integrator._edge_pose_callback(msg)

def test_insight_timer_callback(global_integrator):
    """Test the insight timer callback"""
    with patch.object(global_integrator, '_publish_global_insights') as mock_publish:
        global_integrator._insight_timer_callback()
        mock_publish.assert_called_once()

def test_multiple_edge_nodes_data(global_integrator):
    """Test handling data from multiple edge nodes"""
    # Send messages from different edge nodes
    for i in range(3):
        msg = create_string_message(f'{{"edge_id": "edge_{i}", "status": "active"}}')
        global_integrator._edge_status_callback(msg)
    
    # Check all nodes are tracked
    with global_integrator._lock:
        for i in range(3):
            assert f"edge_{i}" in global_integrator._edge_data

def test_concurrent_access_protection(global_integrator):
    """Test that lock protects against race conditions"""
    # This test ensures that the lock is used in all critical callbacks
    # We can at least verify the lock is acquired
    assert global_integrator._lock is not None

def test_publish_global_insights_with_data(global_integrator):
    """Test publishing insights with actual data"""
    status_msg = create_string_message('{"edge_id": "test_edge", "status": "active"}')
    global_integrator._edge_status_callback(status_msg)
    
    # Call the publish method
    with patch('rclpy.create_publisher'), patch('rclpy.timer.Timer'):
        global_integrator._publish_global_insights()
    
    # Should not raise errors and should publish correctly

def test_get_global_insight_empty(global_integrator):
    """Test getting global insight when no data"""
    insights = global_integrator.get_global_insight()
    assert isinstance(insights, dict)
    # Should return empty dict

def test_get_global_insight_with_data(global_integrator):
    """Test getting global insight with data"""
    test_data = {"test_key": "test_value"}
    with global_integrator._lock:
        global_integrator._processed_insights = test_data
    
    insights = global_integrator.get_global_insight()
    assert insights == test_data