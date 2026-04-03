import pytest
from unittest.mock import Mock, patch
from src.embodied_edge_sim.data_flow_visualizer import DataFlowVisualizer

@pytest.fixture
def visualizer():
    with patch('rclpy.init'), patch('rclpy.shutdown'):
        visualizer = DataFlowVisualizer()
        yield visualizer
        visualizer.destroy_node()

def test_visualizer_initialization():
    with patch('rclpy.init'), patch('rclpy.shutdown'):
        v = DataFlowVisualizer()
        assert v is not None
        v.destroy_node()

def test_visualize_flow_clears_markers(visualizer):
    # Setup - add some mock markers
    visualizer.marker_array.markers = [Mock(), Mock()]
    initial_marker_count = len(visualizer.marker_array.markers)
    
    # Mock the publishing to avoid ROS2 context issues
    with patch.object(visualizer.marker_pub, 'publish') as mock_publish:
        visualizer.visualize_flow()
        assert mock_publish.called
        # Check that markers are cleared
        assert len(visualizer.marker_array.markers) == 0

def test_get_node_names_and_namespaces(visualizer):
    result = visualizer.get_node_names_and_namespaces()
    expected = [("/node1", "/"), ("/node2", "/")]
    assert result == expected

def test_publish_node_markers_creates_markers(visualizer):
    with patch.object(visualizer, 'get_node_names_and_namespaces', return_value=[("/node1", "/"), ("/node2", "/")]):
        visualizer._publish_node_markers()
        assert len(visualizer.marker_array.markers) == 2
        marker1 = visualizer.marker_array.markers[0]
        marker2 = visualizer.marker_array.markers[1]
        assert marker1.header.frame_id == "map"
        assert marker1.type == 2  # SPHERE
        assert marker2.header.frame_id == "map"
        assert marker2.type == 2  # SPHERE

def test_publish_node_markers_marker_properties(visualizer):
    with patch.object(visualizer, 'get_node_names_and_namespaces', return_value=[("/node1", "/")]):
        visualizer._publish_node_markers()
        marker = visualizer.marker_array.markers[0]
        assert marker.ns == "nodes"
        assert marker.type == 2  # SPHERE
        assert marker.action == 0  # ADD
        assert marker.scale.x == 0.2
        assert marker.scale.y == 0.2
        assert marker.scale.z == 0.2
        assert marker.color.r == 0.0
        assert marker.color.g == 1.0
        assert marker.color.b == 0.0
        assert marker.color.a == 1.0

def test_publish_connection_markers_exists(visualizer):
    # This is just to test the method exists and can be called
    visualizer._publish_connection_markers()
    # The implementation is empty, so we just verify it runs without error

def test_spin_once(visualizer):
    with patch('rclpy.spin_once') as mock_spin_once:
        visualizer.spin_once()
        mock_spin_once.assert_called_once_with(visualizer, timeout_sec=0.1)

def test_spin(visualizer):
    with patch('rclpy.spin_once') as mock_spin_once, \
         patch('rclpy.ok', side_effect=[True, False]):  # First call returns True, second call False to break loop
        visualizer.spin()
        mock_spin_once.assert_called_with(visualizer, timeout_sec=0.1)

def test_destroy_node_cleans_up_timer(visualizer):
    with patch.object(visualizer.timer, 'destroy') as mock_timer_destroy:
        visualizer.destroy_node()
        mock_timer_destroy.assert_called_once()

def test_destroy_node_super_called(visualizer):
    with patch('rclpy.node.Node.destroy_node', wraps=visualizer.__class__.__bases__[0]().destroy_node) as mock_super_destroy:
        visualizer.destroy_node()
        mock_super_destroy.assert_called_once()

def test_get_clock_returns_clock(visualizer):
    clock = visualizer.get_clock()
    assert clock is not None

def test_marker_id_counter_resets(visualizer):
    # Add some initial markers
    visualizer.marker_id_counter = 5
    visualizer.marker_array.markers.append(Mock())
    
    with patch.object(visualizer.marker_pub, 'publish'):
        visualizer.visualize_flow()
        assert visualizer.marker_id_counter == 0

def test_multiple_nodes_create_multiple_markers(visualizer):
    test_nodes = [("/node1", "/"), ("/node2", "/"), ("/node3", "/")]
    with patch.object(visualizer, 'get_node_names_and_namespaces', return_value=test_nodes):
        visualizer._publish_node_markers()
        assert len(visualizer.marker_array.markers) == 3

def test_empty_node_list(visualizer):
    with patch.object(visualizer, 'get_node_names_and_namespaces', return_value=[]):
        visualizer._publish_node_markers()
        assert len(visualizer.marker_array.markers) == 0

def test_qos_profile_settings(visualizer):
    assert visualizer.qos_profile.reliability == 1  # RELIABLE
    assert visualizer.qos_profile.durability == 2   # TRANSIENT_LOCAL
    assert visualizer.qos_profile.depth == 10

def test_marker_array_is_cleared_each_time(visualizer):
    # Add some mock markers
    visualizer.marker_array.markers = [Mock(), Mock()]
    
    with patch.object(visualizer.marker_pub, 'publish') as mock_publish:
        visualizer.visualize_flow()
        # Check that the marker array is cleared
        assert len(visualizer.marker_array.markers) == 0

def test_node_marker_properties(visualizer):
    with patch.object(visualizer, 'get_node_names_and_namespaces', return_value=[("/node1", "/")]):
        visualizer._publish_node_markers()
        marker = visualizer.marker_array.markers[0]
        assert marker.pose.position.x == 0.0
        assert marker.pose.position.y == 0.0
        assert marker.pose.position.z == 0.0
        assert marker.pose.orientation.x == 0.0
        assert marker.pose.orientation.y == 0.0
        assert marker.pose.orientation.z == 0.0
        assert marker.pose.orientation.w == 1.0

def test_marker_id_increment(visualizer):
    with patch.object(visualizer, 'get_node_names_and_namespaces', return_value=[("/node1", "/"), ("/node2", "/")]):
        initial_counter = visualizer.marker_id_counter
        visualizer._publish_node_markers()
        # Should have incremented by 2
        assert visualizer.marker_id_counter == initial_counter + 2

def test_timer_callback_publishes(visualizer):
    with patch.object(visualizer.marker_pub, 'publish') as mock_publish:
        visualizer.visualize_flow()
        mock_publish.assert_called_once()

def test_node_marker_header(visualizer):
    with patch.object(visualizer, 'get_node_names_and_namespaces', return_value=[("/node1", "/")]):
        visualizer._publish_node_markers()
        marker = visualizer.marker_array.markers[0]
        assert marker.header.frame_id == "map"
        assert marker.ns == "nodes"