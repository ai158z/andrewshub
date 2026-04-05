import pytest
from unittest.mock import patch, MagicMock
from backend.app.utils.ros2_utils import (
    create_ros2_node,
    destroy_ros2_node,
    get_node_status,
    ROS2NodeManager,
)

@pytest.fixture
def manager():
    return ROS2NodeManager()

@pytest.fixture(autouse=True)
def reset_manager():
    # Reset the global manager state before each test
    manager = ROS2NodeManager()
    manager.node = None
    manager.node_initialized = False

@patch('backend.app.utils.ros2_utils.rclpy.init')
@patch('backend.app.utils.ros2_utils.init_ros2_node')
def test_initialize_node_success(mock_init_node, mock_rclpy_init, manager):
    mock_node = MagicMock()
    mock_node.get_name.return_value = 'test_node'
    mock_init_node.return_value = mock_node
    
    result = manager.initialize_node('test_node')
    
    assert result is True
    assert manager.node_initialized is True
    assert manager.node == mock_node
    mock_rclpy_init.assert_called_once()
    mock_init_node.assert_called_once_with('test_node')

@patch('backend.app.utils.ros2_utils.rclpy.init')
@patch('backend.app.utils.ros2_utils.rclpy.shutdown')
@patch('backend.app.utils.ros2_utils.init_ros2_node')
def test_cleanup_node_success(mock_init_node, mock_shutdown, mock_init, manager):
    # Setup: Initialize node first
    mock_node = MagicMock()
    mock_node.get_name.return_value = 'test_node'
    mock_init_node.return_value = mock_node
    manager.node = mock_node
    manager.node_initialized = True
    
    result = manager.cleanup_node()
    
    assert result is True
    assert manager.node_initialized is False
    mock_shutdown.assert_called_once()

def test_get_status_initialized(manager):
    manager.node_initialized = True
    manager.node = MagicMock()
    manager.node.get_name.return_value = 'test_node'
    
    status = manager.get_status()
    
    assert status['initialized'] is True
    assert status['node'] == 'test_node'

def test_get_status_not_initialized(manager):
    status = manager.get_status()
    
    assert status['initialized'] is False
    assert status['node'] is None

@patch('backend.app.utils.ros2_utils.rclpy.init')
@patch('backend.app.utils.ros2_utils.init_ros2_node')
def test_create_ros2_node_success(mock_init_node, mock_rclpy_init):
    mock_node = MagicMock()
    mock_init_node.return_value = mock_node
    
    result = create_ros2_node('test_node')
    
    assert result is True
    # Verify the global manager state
    status = get_node_status()
    assert status['initialized'] is True

@patch('backend.app.utils.ros2_utils.rclpy.init')
@patch('backend.app.utils.ros2_utils.rclpy.shutdown')
def test_destroy_ros2_node_success(mock_shutdown, mock_init):
    # Setup: Initialize first
    with patch('backend.app.utils.ros2_utils._node_manager.node_initialized', True):
        result = destroy_ros2_node()
        assert result is True

def test_get_node_status():
    status = get_node_status()
    assert 'initialized' in status
    assert 'node' in status

@patch('backend.app.utils.ros2_utils.rclpy.init')
@patch('backend.app.utils.ros2_utils.init_ros2_node')
def test_initialize_node_when_already_initialized(mock_init_node, mock_rclpy_init, manager):
    # First initialization
    mock_node = MagicMock()
    mock_init_node.return_value = mock_node
    
    result1 = manager.initialize_node('test_node')
    assert result1 is True
    
    # Second initialization should return True without re-initializing
    result2 = manager.initialize_node('test_node')
    assert result2 is True
    # init should only be called once
    mock_init_node.assert_called_once()

@patch('backend.app.utils.ros2_utils.rclpy.init')
@patch('backend.app.utils.ros2_utils.rclpy.shutdown')
@patch('backend.app.utils.ros2_utils.init_ros2_node')
def test_cleanup_when_not_initialized(mock_init_node, mock_shutdown, mock_init, manager):
    result = manager.cleanup_node()
    assert result is True  # Should return True even when not initialized
    mock_shutdown.assert_not_called()

@patch('backend.app.utils.ros2_utils.rclpy.init')
@patch('backend.app.utils.ros2_utils.init_ros2_node')
def test_multiple_initialize_calls(mock_init_node, mock_rclpy_init, manager):
    mock_node = MagicMock()
    mock_init_node.return_value = mock_node
    
    manager.initialize_node('test_node')
    # Second call when already initialized
    result = manager.initialize_node('test_node2')
    assert result is True
    # init_ros2_node should only be called once
    mock_init_node.assert_called_once()

@patch('backend.app.utils.ros2_utils.rclpy.init')
@patch('backend.app.utils.ros2_utils.init_ros2_node')
def test_initialize_node_exception_handling(mock_init_node, mock_rclpy_init, manager):
    mock_rclpy_init.side_effect = Exception("ROS2 init failed")
    
    result = manager.initialize_node('test_node')
    assert result is False
    assert manager.node_initialized is False

@patch('backend.app.utils.ros2_utils.rclpy.init')
@patch('backend.app.utils.ros2_utils.rclpy.shutdown')
def test_cleanup_node_exception_handling(mock_shutdown, mock_init, manager):
    mock_shutdown.side_effect = Exception("Shutdown error")
    manager.node_initialized = True
    
    result = manager.cleanup_node()
    assert result is False

def test_get_status_with_none_node(manager):
    status = manager.get_status()
    assert status['node'] is None

@patch('backend.app.utils.ros2_utils.rclpy.init')
def test_create_ros2_node_failure(mock_init, manager):
    mock_init.side_effect = Exception("Init error")
    
    result = manager.initialize_node()
    assert result is False

@patch('backend.app.utils.ros2_utils.rclpy.init')
@patch('backend.app.utils.ros2_utils.init_ros2_node')
def test_get_status_after_init(mock_init_node, mock_init, manager):
    mock_node = MagicMock()
    mock_node.get_name.return_value = 'status_test_node'
    mock_init_node.return_value = mock_node
    
    manager.initialize_node('status_test_node')
    status = manager.get_status()
    
    assert status['initialized'] is True
    assert status['node'] == 'status_test_node'

def test_get_node_status_consistency():
    status = get_node_status()
    assert isinstance(status, dict)
    assert 'initialized' in status
    assert 'node' in status

@patch('backend.app.utils.ros2_utils.rclpy.init')
@patch('backend.app.utils.ros2_utils.init_ros2_node')
def test_create_ros2_node_function(mock_init_node, mock_init):
    mock_node = MagicMock()
    mock_init_node.return_value = mock_node
    
    result = create_ros2_node('function_test')
    assert result is True
    
    status = get_node_status()
    assert status['initialized'] is True

@patch('backend.app.utils.ros2_utils.rclpy.shutdown')
def test_destroy_ros2_node_function(mock_shutdown):
    with patch('backend.app.utils.ros2_utils._node_manager.node_initialized', True):
        result = destroy_ros2_node()
        assert result is True

@patch('backend.app.utils.ros2_utils.rclpy.init')
@patch('backend.app.utils.ros2_utils.init_ros2_node')
def test_node_manager_state_persists(mock_init_node, mock_init):
    mock_node = MagicMock()
    mock_init_node.return_value = mock_node
    
    create_ros2_node('state_test')
    
    status = get_node_status()
    assert status['initialized'] is True
    
    # Clean up
    destroy_ros2_node()
    
    final_status = get_node_status()
    assert final_status['initialized'] is False