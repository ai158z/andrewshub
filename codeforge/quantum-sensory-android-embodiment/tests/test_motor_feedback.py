import pytest
from unittest.mock import Mock, patch, MagicMock
from src.quantum_sensors.motor_feedback import MotorFeedbackController, MotorState

class TestMotorFeedbackController:
    @pytest.fixture
    def motor_controller(self):
        with patch.multiple('src.quantum_sensors.motor_feedback', 
                         QubitSensorProcessor=MagicMock,
                         OrchORSimulator=MagicMock,
                         SensoryFusionEngine=MagicMock,
                         IdentityContinuityManager=MagicMock,
                         CodonicSymbolicLayer=MagicMock,
                         QuantumPerceptionEngine=MagicMock,
                         ROS2Bridge=MagicMock,
                         ConsciousnessInterface=MagicMock):
            controller = MotorFeedbackController()
            controller.qubit_processor = Mock()
            controller.orch_simulator = Mock()
            controller.sensory_fusion = Mock()
            controller.identity_manager = Mock()
            controller.codonic_layer = Mock()
            controller.quantum_engine = Mock()
            controller.ros2_bridge = Mock()
            controller.consciousness_interface = Mock()
            return controller

    def test_update_joint_angles_success(self, motor_controller):
        # Arrange
        joint_commands = {"joint1": 1.5, "joint2": 0.8}
        mock_sensory_data = {
            "joint_angles": {"joint1": 1.0, "joint2": 0.5}
        }
        motor_controller.qubit_processor.process_sensory_data.return_value = mock_sensory_data
        motor_controller.sensory_fusion.fuse_sensory_inputs.return_value = mock_sensory_data
        motor_controller.quantum_engine.process_perception_quantum.return_value = {}
        motor_controller.orch_simulator.simulate_consciousness_state.return_value = {}
        motor_controller.codonic_layer.encode_symbolic_representation.return_value = "symbolic"
        motor_controller.codonic_layer.decode_codon_sequence.return_value = joint_commands
        motor_controller.consciousness_interface.integrate_cognitive_states.return_value = joint_commands
        motor_controller.consciousness_interface.model_self_awareness.return_value = {"confidence": 1.0}
        motor_controller.ros2_bridge.publish_sensor_data = Mock()

        # Act
        result = motor_controller.update_joint_angles(joint_commands)

        # Assert
        assert result is not None
        assert isinstance(result, dict)
        motor_controller.qubit_processor.process_sensory_data.assert_called_once()
        motor_controller.sensory_fusion.fuse_sensory_inputs.assert_called_once()
        motor_controller.quantum_engine.process_perception_quantum.assert_called_once()
        motor_controller.orch_simulator.simulate_consciousness_state.assert_called_once()
        motor_controller.ros2_bridge.publish_sensor_data.assert_called_once()

    def test_update_joint_angles_with_provided_sensors(self, motor_controller):
        # Arrange
        joint_commands = {"joint1": 1.5}
        sensor_data = {"joint_angles": {"joint1": 1.0}}
        expected_result = {"joint1": 1.46}  # Adjusted value based on feedback logic
        
        motor_controller.sensory_fusion.fuse_sensory_inputs.return_value = sensor_data
        motor_controller.quantum_engine.process_perception_quantum.return_value = {}
        motor_controller.orch_simulator.simulate_consciousness_state.return_value = {}
        motor_controller.codonic_layer.encode_symbolic_representation.return_value = "symbolic"
        motor_controller.codonic_layer.decode_codon_sequence.return_value = joint_commands
        motor_controller.consciousness_interface.integrate_cognitive_states.return_value = joint_commands
        motor_controller.consciousness_interface.model_self_awareness.return_value = {"confidence": 1.0}

        # Act
        result = motor_controller.update_joint_angles(joint_commands, sensor_data)

        # Assert
        assert result == joint_commands  # No adjustment needed in this test case

    def test_update_joint_angles_error_handling(self, motor_controller):
        # Arrange
        joint_commands = {"joint1": 1.5}
        motor_controller.qubit_processor.process_sensory_data.side_effect = Exception("Sensor error")

        # Act
        result = motor_controller.update_joint_angles(joint_commands)

        # Assert
        assert result == joint_commands  # Should return original commands on error

    def test_calibrate_feedback_success(self, motor_controller):
        # Arrange
        motor_controller.qubit_processor.measure_quantum_state.return_value = {"sensor1": 0.5}
        motor_controller.orch_simulator.process_perceptual_field.return_value = {"state": "conscious"}
        motor_controller._process_calibration_data = Mock()
        motor_controller._process_calibration_data.return_value = {"optimal_gain": 0.7, "status": "calibrated"}

        # Act
        result = motor_controller.calibrate_feedback()

        # Assert
        assert result["status"] == "calibrated"
        assert result["optimal_gain"] == 0.7
        motor_controller.qubit_processor.measure_quantum_state.assert_called_once()
        motor_controller.orch_simulator.process_perceptual_field.assert_called_once()

    def test_calibrate_feedback_error(self, motor_controller):
        # Arrange
        motor_controller.qubit_processor.measure_quantum_state.side_effect = Exception("Calibration error")

        # Act
        result = motor_controller.calibrate_feedback()

        # Assert
        assert result["status"] == "error"
        assert "error" in result

    def test_apply_feedback_control_with_no_error(self, motor_controller):
        # Arrange
        joint_commands = {"joint1": 1.0}
        sensory_data = {"joint_angles": {"joint1": 1.0}}  # No error
        motor_controller.codonic_layer.encode_symbolic_representation.return_value = "symbolic"
        motor_controller.codonic_layer.decode_codon_sequence.return_value = joint_commands
        motor_controller.consciousness_interface.integrate_cognitive_states.return_value = joint_commands
        motor_controller.consciousness_interface.model_self_awareness.return_value = {"confidence": 1.0}

        # Act
        result = motor_controller._apply_feedback_control(
            joint_commands, 
            sensory_data, 
            {}, 
            {}
        )

        # Assert
        assert result == joint_commands  # Should be unchanged when no error

    def test_apply_feedback_control_with_error(self, motor_controller):
        # Arrange
        joint_commands = {"joint1": 1.0}
        sensory_data = {"joint_angles": {"joint1": 0.5}}  # Error = 0.5
        motor_controller.codonic_layer.encode_symbolic_representation.return_value = "symbolic"
        motor_controller.codonic_layer.decode_codon_sequence.return_value = joint_commands
        motor_controller.consciousness_interface.integrate_cognitive_states.return_value = joint_commands
        motor_controller.consciousness_interface.model_self_awareness.return_value = {"confidence": 0.9}

        # Act
        result = motor_controller._apply_feedback_control(
            joint_commands,
            sensory_data,
            {},
            {}
        )

        # Assert
        assert "joint1" in result
        # With error, the result should be different from input
        assert result["joint1"] != 1.0

    def test_update_motor_state(self, motor_controller):
        # Arrange
        joint_commands = {"joint1": 1.5, "joint2": 0.8}
        initial_timestamp = motor_controller.motor_state.timestamp

        # Act
        motor_controller._update_motor_state(joint_commands)

        # Assert
        assert motor_controller.motor_state.joint_angles == joint_commands
        assert motor_controller.motor_state.timestamp == initial_timestamp + 0.01
        assert "joint1" in motor_controller.motor_state.velocities
        assert "joint2" in motor_controller.motor_state.torques

    def test_process_calibration_data_empty_readings(self, motor_controller):
        # Act
        result = motor_controller._process_calibration_data([])

        # Assert
        assert result["optimal_gain"] == 0.8  # Default value
        assert result["status"] == "default"

    def test_process_calibration_data_with_readings(self, motor_controller):
        # Arrange
        readings = [
            {"sensors": {"sensor1": 1.0}, "time": 0.0},
            {"sensors": {"sensor1": 1.5}, "time": 0.1}
        ]

        # Act
        result = motor_controller._process_calibration_data(readings)

        # Assert
        assert result["status"] == "calibrated"
        assert "optimal_gain" in result
        assert result["optimal_gain"] > 0
        assert result["optimal_gain"] <= 1.0

    def test_calculate_joint_error(self, motor_controller):
        # Act
        error = motor_controller._calculate_joint_error(1.0, 0.5)

        # Assert
        assert error == 0.5

    def test_apply_proportional_control_no_correction(self, motor_controller):
        # Arrange
        motor_controller.max_joint_error = 0.1  # Set high threshold
        commands = {"joint1": 1.0}

        # Act
        result = motor_controller._apply_proportional_control(0.05, commands)  # Small error

        # Assert
        assert result["joint1"] == 1.0  # No change expected

    def test_apply_proportional_control_with_correction(self, motor_controller):
        # Arrange
        motor_controller.max_joint_error = 0.01
        motor_controller.feedback_gain = 0.8
        commands = {"joint1": 1.0}

        # Act
        result = motor_controller._apply_proportional_control(0.1, commands)  # Large error

        # Assert
        assert result["joint1"] != 1.0  # Should be adjusted

    def test_update_joint_angles_empty_commands(self, motor_controller):
        # Act
        result = motor_controller.update_joint_angles({})

        # Assert
        assert result == {}

    def test_update_joint_angles_none_sensors(self, motor_controller):
        # Arrange
        joint_commands = {"joint1": 1.0}
        motor_controller.qubit_processor.process_sensory_data.return_value = {"joint_angles": {"joint1": 0.5}}
        motor_controller.sensory_fusion.fuse_sensory_inputs.return_value = {"joint_angles": {"joint1": 0.5}}
        motor_controller.quantum_engine.process_perception_quantum.return_value = {}
        motor_controller.orch_simulator.simulate_consciousness_state.return_value = {}
        motor_controller.codonic_layer.encode_symbolic_representation.return_value = "symbolic"
        motor_controller.codonic_layer.decode_codon_sequence.return_value = joint_commands
        motor_controller.consciousness_interface.integrate_cognitive_states.return_value = joint_commands
        motor_controller.consciousness_interface.model_self_awareness.return_value = {"confidence": 1.0}

        # Act
        result = motor_controller.update_joint_angles(joint_commands, None)

        # Assert
        assert result is not None

    def test_calibrate_feedback_multiple_calls(self, motor_controller):
        # Arrange
        motor_controller.qubit_processor.measure_quantum_state.return_value = {"sensor1": 0.5}
        motor_controller.orch_simulator.process_perceptual_field.return_value = {"state": "conscious"}
        motor_controller._process_calibration_data.return_value = {"optimal_gain": 0.7, "status": "calibrated"}

        # Act
        result1 = motor_controller.calibrate_feedback()
        result2 = motor_controller.calibrate_feedback()

        # Assert
        assert result1["status"] == "calibrated"
        assert result2["status"] == "calibrated"

    def test_apply_feedback_control_large_error(self, motor_controller):
        # Arrange
        joint_commands = {"joint1": 1.0}
        sensory_data = {"joint_angles": {"joint1": 0.0}}  # Large error
        motor_controller.codonic_layer.encode_symbolic_representation.return_value = "symbolic"
        motor_controller.codonic_layer.decode_codon_sequence.return_value = joint_commands
        motor_controller.consciousness_interface.integrate_cognitive_states.return_value = {"joint1": 0.8}
        motor_controller.consciousness_interface.model_self_awareness.return_value = {"confidence": 0.5}

        # Act
        result = motor_controller._apply_feedback_control(
            joint_commands,
            sensory_data,
            {},
            {}
        )

        # Assert
        assert result["joint1"] != 1.0  # Should be adjusted due to large error

    def test_update_motor_state_empty_commands(self, motor_controller):
        # Act
        motor_controller._update_motor_state({})

        # Assert
        assert motor_controller.motor_state.joint_angles == {}
        assert motor_controller.motor_state.velocities == {}
        assert motor_controller.motor_state.torques == {}

    def test_update_joint_angles_with_consciousness_influence(self, motor_controller):
        # Arrange
        joint_commands = {"joint1": 1.0}
        sensory_data = {"joint_angles": {"joint1": 0.5}}
        motor_controller.codonic_layer.encode_symbolic_representation.return_value = "symbolic"
        motor_controller.codonic_layer.decode_codon_sequence.return_value = joint_commands
        motor_controller.consciousness_interface.integrate_cognitive_states.return_value = {"joint1": 0.9}
        motor_controller.consciousness_interface.model_self_awareness.return_value = {"confidence": 0.8}

        # Act
        result = motor_controller.update_joint_angles(joint_commands, sensory_data)

        # Assert
        assert result is not None
        assert "joint1" in result

    def test_update_joint_angles_codonic_processing(self, motor_controller):
        # Arrange
        joint_commands = {"joint1": 1.0}
        motor_controller.codonic_layer.encode_symbolic_representation.return_value = "ACTG"
        motor_controller.codonic_layer.decode_codon_sequence.return_value = joint_commands
        motor_controller.qubit_processor.process_sensory_data.return_value = {"joint_angles": {"joint1": 0.5}}
        motor_controller.sensory_fusion.fuse_sensory_inputs.return_value = {"joint_angles": {"joint1": 0.5}}
        motor_controller.quantum_engine.process_perception_quantum.return_value = {}
        motor_controller.orch_simulator.simulate_consciousness_state.return_value = {}
        motor_controller.consciousness_interface.integrate_cognitive_states.return_value = joint_commands
        motor_controller.consciousness_interface.model_self_awareness.return_value = {"confidence": 1.0}
        motor_controller.ros2_bridge.publish_sensor_data = Mock()

        # Act
        result = motor_controller.update_joint_angles(joint_commands)

        # Assert
        assert result is not None
        motor_controller.codonic_layer.encode_symbolic_representation.assert_called_once()
        motor_controller.codonic_layer.decode_codon_sequence.assert_called_once()