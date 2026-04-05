import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import json

from backend.app.ros2_bridge import (
    ROS2BridgeNode,
    init_ros2_node,
    get_agent_status,
    get_system_metrics,
)

@pytest.fixture
def mock_rclpy():
    with patch("backend.app.ros2_bridge.rclpy") as mock_rclpy:
        mock_rclpy.init = MagicMock()
        mock_rclpy.create_node = MagicMock()
        yield mock_rclpy

@pytest.fixture
def mock_db_session():
    with patch("backend.app.ros2_bridge.get_db") as mock_get_db:
        mock_session = MagicMock()
        mock_get_db.return_value = iter([mock_session])
        yield mock_session

def test_ros2_bridge_node_initialization(mock_rclpy):
    with patch("backend.app.ros2_bridge.Settings", return_value=MagicMock()):
        node = ROS2BridgeNode("test_node")
        assert node is not None

def test_command_callback_valid_json():
    node = MagicMock()
    msg = MagicMock()
    msg.data = '{"command": "test"}'
    with patch("backend.app.ros2_bridge.json.loads") as mock_loads:
        mock_loads.return_value = {"command": "test"}
        node.command_callback(msg)
        mock_loads.assert_called_once_with('{"command": "test"}')

def test_command_callback_invalid_json():
    node = MagicMock()
    msg = MagicMock()
    msg.data = "invalid json"
    with patch("backend.app.ros2_bridge.ROS2BridgeNode.get_logger") as mock_logger:
        mock_logger.error = MagicMock()
        node.get_logger.return_value = mock_logger
        node.command_callback(msg)
        mock_logger.error.assert_called()

def test_timer_callback_publishes_metrics():
    node = MagicMock()
    with patch.object(node, 'get_system_metrics', return_value={"test": "data"}), \
         patch.object(node, 'status_publisher'), \
         patch("backend.app.ros2_bridge.String") as mock_string:
        node.timer_callback()
        mock_string.assert_called()

def test_get_system_metrics():
    metrics = get_system_metrics()
    assert "timestamp" in metrics
    assert "cpu_percent" in metrics

def test_get_agent_status_with_valid_agent(mock_db_session):
    mock_agent = MagicMock()
    mock_agent.id = "agent1"
    mock_agent.name = "Test Agent"
    mock_agent.status = "active"
    mock_agent.last_seen = datetime.now()
    mock_agent.is_active = True
    mock_db_session.return_value = mock_db_session
    with patch("backend.app.ros2_bridge.get_agent_by_id", return_value=mock_agent):
        result = get_agent_status("agent1")
        assert result["agent_id"] == "agent1"

def test_get_agent_status_with_invalid_agent(mock_db_session):
    mock_db_session.return_value = mock_db_session
    with patch("backend.app.ros2_bridge.get_agent_by_id", return_value=None):
        result = get_agent_status("invalid")
        assert result == {"error": "Agent not found"}

def test_get_agent_status_exception_handling(mock_db_session):
    mock_db_session.return_value = mock_db_session
    with patch("backend.app.ros2_bridge.get_agent_by_id", side_effect=Exception("DB Error")):
        result = get_agent_status("agent1")
        assert result == {"error": "DB Error"}

def test_init_ros2_node_success(mock_rclpy):
    with patch("backend.app.ros2_bridge.rclpy.init"), \
         patch("backend.app.ros2_bridge.rclpy.ok", return_value=True):
        node = init_ros2_node()
        assert node is not None

def test_init_ros2_node_failure():
    with patch("backend.app.ros2_bridge.rclpy.init", side_effect=Exception("Init failed")):
        node = init_ros2_node()
        assert node is None

def test_process_command():
    node = MagicMock()
    command_data = {"command": "test"}
    node.process_command(command_data)
    assert True

def test_get_system_metrics_structure():
    metrics = get_system_metrics()
    assert "timestamp" in metrics
    assert "cpu_percent" in metrics
    assert "memory_percent" in metrics
    assert "disk_usage" in metrics
    assert "network_io" in metrics

def test_get_agent_status_func_with_valid_agent():
    with patch("backend.app.ros2_bridge.get_agent_by_id") as mock_get_agent:
        mock_agent = MagicMock()
        mock_agent.id = "agent1"
        mock_agent.name = "Test Agent"
        mock_agent.status = "active"
        mock_agent.last_seen = "2023-01-01T00:00:00"
        mock_agent.is_active = True
        mock_get_agent.return_value = mock_agent
        result = get_agent_status("agent1")
        assert result["agent_id"] == "agent1"
        assert result["name"] == "Test Agent"
        assert result["status"] == "active"
        assert result["is_active"] is True

def test_get_agent_status_func_agent_not_found():
    with patch("backend.app.ros2_bridge.get_agent_by_id", return_value=None):
        result = get_agent_status("invalid")
        assert result == {"error": "Agent not found"}

def test_get_agent_status_func_exception():
    with patch("backend.app.ros2_bridge.get_agent_by_id", side_effect=Exception("Test error")):
        result = get_agent_status("test")
        assert result == {"error": "Test error"}

def test_command_callback_json_decode_error():
    node = MagicMock()
    msg = MagicMock()
    msg.data = "invalid json"
    with patch("backend.app.ros2_bridge.json.JSONDecodeError"):
        node.command_callback(msg)
        node.get_logger().error.assert_called()

def test_command_callback_general_exception():
    node = MagicMock()
    msg = MagicMock()
    msg.data = '{"command": "test"}'
    with patch("backend.app.ros2_bridge.json.loads", return_value={"command": "test"}), \
         patch.object(node, 'process_command', side_effect=Exception("Processing error")):
        node.command_callback(msg)
        node.get_logger().error.assert_called()

def test_timer_callback_publishes_string_message():
    node = MagicMock()
    with patch.object(node, 'get_system_metrics', return_value={"test": "data"}), \
         patch("backend.app.ros2_bridge.String") as mock_string:
        node.timer_callback()
        mock_string.assert_called()

def test_get_system_metrics_returns_dict():
    result = get_system_metrics()
    assert isinstance(result, dict)

def test_get_agent_status_returns_dict():
    with patch("backend.app.ros2_bridge.get_agent_by_id", return_value=None):
        result = get_agent_status("test")
        assert isinstance(result, dict)