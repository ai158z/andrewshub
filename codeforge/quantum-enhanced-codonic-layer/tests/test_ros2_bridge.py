import pytest
from unittest.mock import Mock, patch, MagicMock
from codonic_layer.ros2_bridge import ROS2Bridge
from std_msgs.msg import String
import json


@pytest.fixture
def ros2_bridge():
    with patch('rclpy.node.Node.__init__'):
        bridge = ROS2Bridge()
        bridge.get_clock = Mock()
        bridge.get_clock.return_value = Mock()
        bridge.get_clock.return_value.now.return_value = Mock(nanoseconds=123456789)
        return bridge


def test_init_creates_empty_publishers_and_subscriptions(ros2_bridge):
    assert ros2_bridge._publishers == {}
    assert ros2_bridge._subscriptions == {}


def test_create_quantum_publisher_creates_new_publisher(ros2_bridge):
    with patch.object(ros2_bridge, 'create_publisher') as mock_create:
        mock_publisher = Mock()
        mock_create.return_value = mock_publisher
        
        publisher = ros2_bridge.create_quantum_publisher('/test_topic')
        
        assert publisher == mock_publisher
        assert ros2_bridge._publishers['/test_topic'] == publisher


def test_create_quantum_publisher_returns_existing_publisher(ros2_bridge):
    existing_publisher = Mock()
    ros2_bridge._publishers['/test_topic'] = existing_publisher
    
    publisher = ros2_bridge.create_quantum_publisher('/test_topic')
    
    assert publisher == existing_publisher


def test_create_interference_subscription_creates_new_subscription(ros2_bridge):
    with patch.object(ros2_bridge, 'create_subscription') as mock_create:
        mock_subscription = Mock()
        mock_create.return_value = mock_subscription
        
        subscription = ros2_bridge.create_interference_subscription(
            '/test_topic', Mock()
        )
        
        assert subscription == mock_subscription
        assert ros2_bridge._subscriptions['/test_topic'] == subscription


def test_create_interference_subscription_returns_existing_subscription(ros2_bridge):
    existing_subscription = Mock()
    ros2_bridge._subscriptions['/test_topic'] = existing_subscription
    
    subscription = ros2_bridge.create_interference_subscription(
        '/test_topic', Mock()
    )
    
    assert subscription == existing_subscription


def test_publish_quantum_state_validates_type(ros2_bridge):
    class MockQuantumStates:
        def get_state(self):
            return "test_state"
    
    with pytest.raises(TypeError, match="State must be an instance of QuantumStates"):
        ros2_bridge.publish_quantum_state(MockQuantumStates())


def test_publish_quantum_state_creates_publisher_if_not_exists(ros2_bridge):
    mock_states = Mock()
    mock_states.get_state.return_value = Mock()
    mock_states.get_state.return_value.tolist.return_value = [1, 0]
    
    with patch.object(ros2_bridge, 'create_publisher') as mock_create:
        mock_publisher = Mock()
        mock_create.return_value = mock_publisher
        
        ros2_bridge.publish_quantum_state(mock_states, '/quantum_state')
        
        mock_create.assert_called_once()


def test_publish_quantum_state_publishes_serialized_data(ros2_bridge):
    mock_states = Mock()
    mock_states.get_state.return_value = Mock()
    mock_states.get_state.return_value.tolist.return_value = [1, 0]
    
    with patch.object(ros2_bridge, 'create_publisher') as mock_create:
        mock_publisher = Mock()
        mock_create.return_value = mock_publisher
        ros2_bridge._publishers['/quantum_state'] = mock_publisher
        
        ros2_bridge.publish_quantum_state(mock_states, '/quantum_state')
        
        mock_publisher.publish.assert_called_once()
        call_args = mock_publisher.publish.call_args[0][0]
        assert isinstance(call_args, String)
        data = json.loads(call_args.data)
        assert 'state_vector' in data
        assert 'timestamp' in data
        assert 'state_type' in data


def test_subscribe_interference_creates_subscription(ros2_bridge):
    callback = Mock()
    with patch.object(ros2_bridge, 'create_subscription') as mock_create:
        mock_subscription = Mock()
        mock_create.return_value = mock_subscription
        
        ros2_bridge.subscribe_interference('/interference', callback)
        
        mock_create.assert_called_once()


def test_subscribe_interference_uses_default_callback(ros2_bridge):
    mock_states = Mock()
    ros2_bridge._quantum_states = mock_states
    
    with patch.object(ros2_bridge, 'create_subscription') as mock_create:
        mock_subscription = Mock()
        mock_create.return_value = mock_subscription
        ros2_bridge._subscriptions['/interference'] = mock_subscription
        
        ros2_bridge.subscribe_interference('/interference')
        
        # Verify the subscription was created with a callback
        mock_create.assert_called_once()


def test_initialize_quantum_system_sets_components(ros2_bridge):
    ros2_bridge.initialize_quantum_system()
    
    assert ros2_bridge._quantum_states is not None
    assert ros2_bridge._interference_tracker is not None


def test_initialize_quantum_system_handles_exception(ros2_bridge):
    with patch('codonic_layer.ros2_bridge.QuantumStates') as mock_quantum_states, \
         patch('codonic_layer.ros2_bridge.InterferenceTracker') as mock_interference_tracker:
        
        mock_quantum_states.side_effect = Exception("Init failed")
        mock_interference_tracker.return_value = Mock()
        
        with pytest.raises(Exception, match="Init failed"):
            ros2_bridge.initialize_quantum_system()


def test_set_quantum_states_validates_type(ros2_bridge):
    with pytest.raises(TypeError, match="States must be an instance of QuantumStates"):
        ros2_bridge.set_quantum_states("invalid")


def test_set_quantum_states_accepts_valid_type(ros2_bridge):
    quantum_states = Mock()
    ros2_bridge.set_quantum_states(quantum_states)
    assert ros2_bridge._quantum_states == quantum_states


def test_set_interference_tracker_validates_type(ros2_bridge):
    with pytest.raises(TypeError, match="Tracker must be an instance of InterferenceTracker"):
        ros2_bridge.set_interference_tracker("invalid")


def test_set_interference_tracker_accepts_valid_type(ros2_bridge):
    tracker = Mock()
    ros2_bridge.set_interference_tracker(tracker)
    assert ros2_bridge._interference_tracker == tracker


def test_get_quantum_publisher_returns_existing(ros2_bridge):
    publisher = Mock()
    ros2_bridge._publishers['test'] = publisher
    assert ros2_bridge.get_quantum_publisher('test') == publisher


def test_get_quantum_publisher_returns_none_for_nonexistent(ros2_bridge):
    assert ros2_bridge.get_quantum_publisher('nonexistent') is None


def test_get_interference_subscription_returns_existing(ros2_bridge):
    subscription = Mock()
    ros2_bridge._subscriptions['test'] = subscription
    assert ros2_bridge.get_interference_subscription('test') == subscription


def test_get_interference_subscription_returns_none_for_nonexistent(ros2_bridge):
    assert ros2_bridge.get_interference_subscription('nonexistent') is None


def test_cleanup_clears_resources(ros2_bridge):
    ros2_bridge._publishers['test'] = Mock()
    ros2_bridge._subscriptions['test'] = Mock()
    ros2_bridge._quantum_states = Mock()
    ros2_bridge._interference_tracker = Mock()
    
    ros2_bridge.cleanup()
    
    assert ros2_bridge._publishers == {}
    assert ros2_bridge._subscriptions == {}
    assert ros2_bridge._quantum_states is None
    assert ros2_bridge._interference_tracker is None