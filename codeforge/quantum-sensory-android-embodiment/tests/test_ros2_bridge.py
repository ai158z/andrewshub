import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from src.quantum_sensors.ros2_bridge import ROS2Bridge

@pytest.fixture
def ros2_bridge():
    with patch('rclpy.node.Node.__init__'):
        with patch('rclpy.node.Node.create_publisher'):
            with patch('rclpy.node.Node.create_subscription'):
                bridge = ROS2Bridge()
                bridge.logger = Mock()
                return bridge

def test_init_ros2_bridge(ros2_bridge):
    assert ros2_bridge is not None

def test_motor_command_callback_valid_json(ros2_bridge):
    msg = Mock()
    msg.data = '{"joint_angles": [1.0, 2.0, 3.0], "calibration": true}'
    
    with patch.object(ros2_bridge, '_process_motor_command') as mock_process:
        ros2_bridge._motor_command_callback(msg)
        mock_process.assert_called_once_with({"joint_angles": [1.0, 2.0, 3.0], "calibration": True})

def test_motor_command_callback_invalid_json(ros2_bridge):
    msg = Mock()
    msg.data = '{"invalid_json": }'
    
    with patch('logging.getLogger') as mock_logger:
        mock_logger.return_value = Mock()
        ros2_bridge._motor_command_callback(msg)
        mock_logger.return_value.error.assert_called()

def test_process_motor_command_with_joint_angles(ros2_bridge):
    command_data = {"joint_angles": [1.0, 2.0, 3.0]}
    
    with patch.object(ros2_bridge.motor_controller, 'update_joint_angles') as mock_update:
        ros2_bridge._process_motor_command(command_data)
        mock_update.assert_called_once_with([1.0, 2.0, 3.0])

def test_process_motor_command_with_calibration(ros2_bridge):
    command_data = {"calibration": True}
    
    with patch.object(ros2_bridge.motor_controller, 'calibrate_feedback') as mock_calibrate:
        ros2_bridge._process_motor_command(command_data)
        mock_calibrate.assert_called_once()

def test_process_motor_command_both_parameters(ros2_bridge):
    command_data = {"joint_angles": [1.0, 2.0], "calibration": True}
    
    with patch.object(ros2_bridge.motor_controller, 'update_joint_angles') as mock_update:
        with patch.object(ros2_bridge.motor_controller, 'calibrate_feedback') as mock_calibrate:
            ros2_bridge._process_motor_command(command_data)
            mock_update.assert_called_once_with([1.0, 2.0])
            mock_calibrate.assert_called_once()

def test_publish_sensor_data_success(ros2_bridge):
    test_data = {"sensor1": 100, "sensor2": 200}
    
    # Mock all the subsystems
    with patch.object(ros2_bridge.qubit_processor, 'process_sensory_data', return_value=test_data) as mock_process:
        with patch.object(ros2_bridge.qubit_processor, 'measure_quantum_state', return_value=[0.5, 0.5]) as mock_measure:
            with patch.object(ros2_bridge.sensory_fusion, 'fuse_sensory_inputs', return_value=test_data) as mock_fuse:
                with patch.object(ros2_bridge._sensor_publisher, 'publish') as mock_publish:
                    ros2_bridge.publish_sensor_data(test_data)
                    mock_process.assert_called_once()
                    mock_measure.assert_called_once()
                    mock_fuse.assert_called_once()
                    mock_publish.assert_called_once()

def test_publish_sensor_data_with_numpy_array(ros2_bridge):
    test_data = {"sensor1": 100}
    
    # Mock measure_quantum_state to return numpy array
    with patch.object(ros2_bridge.qubit_processor, 'measure_quantum_state', return_value=Mock()) as mock_array:
        mock_array.tolist.return_value = [0.1, 0.9]
        with patch.object(ros2_bridge._sensor_publisher, 'publish') as mock_publish:
            with patch.object(ros2_bridge.sensory_fusion, 'fuse_sensory_inputs', return_value=test_data):
                ros2_bridge.publish_sensor_data(test_data)
                mock_publish.assert_called_once()

def test_publish_sensor_data_exception_handling(ros2_bridge):
    test_data = {"sensor": 100}
    
    with patch.object(ros2_bridge.qubit_processor, 'process_sensory_data', side_effect=Exception("Test exception")):
        with pytest.raises(Exception):
            ros2_bridge.publish_sensor_data(test_data)

def test_subscribe_motor_commands_active(ros2_bridge):
    ros2_bridge._motor_subscription = Mock()
    ros2_bridge.subscribe_motor_commands()  # Should not warn

def test_subscribe_motor_commands_inactive(ros2_bridge):
    ros2_bridge._motor_subscription = None
    with patch.object(ros2_bridge.logger, 'warning') as mock_warning:
        ros2_bridge.subscribe_motor_commands()
        mock_warning.assert_called_once_with("Motor command subscription is not active")

def test_destroy_node(ros2_bridge):
    with patch('rclpy.node.Node.destroy_node') as mock_destroy:
        ros2_bridge.destroy_node()
        mock_destroy.assert_called_once()

def test_init_ros2_components(ros2_bridge):
    with patch('rclpy.node.Node.create_publisher') as mock_publisher:
        with patch('rclpy.node.Node.create_subscription') as mock_subscription:
            ros2_bridge._init_ros2_components()
            mock_publisher.assert_called_once()
            mock_subscription.assert_called_once()

def test_motor_command_callback_json_error(ros2_bridge):
    msg = Mock()
    msg.data = 'invalid json'
    
    with patch.object(ros2_bridge.logger, 'error') as mock_error:
        ros2_bridge._motor_command_callback(msg)
        mock_error.assert_called()

def test_process_motor_command_no_relevant_keys(ros2_bridge):
    command_data = {"irrelevant_key": "value"}
    
    with patch.object(ros2_bridge.motor_controller, 'update_joint_angles') as mock_update:
        with patch.object(ros2_bridge.motor_controller, 'calibrate_feedback') as mock_calibrate:
            ros2_bridge._process_motor_command(command_data)
            mock_update.assert_not_called()
            mock_calibrate.assert_not_called()

def test_process_motor_command_partial_data(ros2_bridge):
    command_data = {"joint_angles": [1.0, 2.0]}
    
    with patch.object(ros2_bridge.motor_controller, 'update_joint_angles') as mock_update:
        ros2_bridge._process_motor_command(command_data)
        mock_update.assert_called_once_with([1.0, 2.0])

def test_process_motor_command_calibration_only(ros2_bridge):
    command_data = {"calibration": True}
    
    with patch.object(ros2_bridge.motor_controller, 'calibrate_feedback') as mock_calibrate:
        ros2_bridge._process_motor_command(command_data)
        mock_calibrate.assert_called_once()

def test_publish_sensor_data_full_integration(ros2_bridge):
    test_data = {"sensor1": 100, "sensor2": 200}
    
    # Mock all subsystem methods to return test data
    with patch.object(ros2_bridge.qubit_processor, 'process_sensory_data', return_value=test_data):
        with patch.object(ros2_bridge.qubit_processor, 'measure_quantum_state', return_value=[0.5, 0.5]):
            with patch.object(ros2_bridge.sensory_fusion, 'fuse_sensory_inputs', return_value=test_data):
                with patch.object(ros2_bridge.consciousness_interface, 'model_self_awareness', return_value={"awareness": 0.8}):
                    with patch.object(ros2_bridge.codonic_layer, 'encode_symbolic_representation', return_value={"symbolic": "data"}):
                        with patch.object(ros2_bridge.quantum_engine, 'process_perception_quantum', return_value={"perception": 0.9}):
                            with patch.object(ros2_bridge.identity_manager, 'maintain_identity'):
                                with patch.object(ros2_bridge.consciousness_interface, 'integrate_cognitive_states', return_value={"integrated": 0.7}):
                                    with patch.object(ros2_bridge._sensor_publisher, 'publish') as mock_publish:
                                        ros2_bridge.publish_sensor_data(test_data)
                                        mock_publish.assert_called_once()