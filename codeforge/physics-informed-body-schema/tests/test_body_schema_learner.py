import pytest
import torch
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.body_schema_learner import BodySchemaLearner

class TestBodySchemaLearner:
    @pytest.fixture
    def body_schema_learner(self):
        # Mock all dependencies
        pinn_model = Mock()
        biomech_constraints = Mock()
        video_analyzer = Mock()
        codonic_layer = Mock()
        physics_constraints = Mock()
        
        # Create instance
        learner = BodySchemaLearner(
            pinn_model=pinn_model,
            biomech_constraints=biomech_constraints,
            video_analyzer=video_analyzer,
            codonic_layer=codonic_layer,
            physics_constraints=physics_constraints
        )
        return learner

    def test_adapt_body_schema_success(self, body_schema_learner):
        # Setup
        sensory_data = torch.randn(10, 3)
        motor_commands = torch.randn(10, 3)
        body_schema_learner.pinn_model.return_value = sensory_data
        body_schema_learner.codonic_layer.predict_sensory_output.return_value = sensory_data
        
        # Execute
        result = body_schema_learner.adapt_body_schema(sensory_data, motor_commands)
        
        # Verify
        assert "adaptation_error" in result
        assert result["model_parameters_updated"] is True

    def test_adapt_body_schema_invalid_input_type(self, body_schema_learner):
        # Setup
        sensory_data = [1, 2, 3]  # Invalid type
        motor_commands = torch.randn(3, 3)
        
        # Execute & Verify
        with pytest.raises(TypeError):
            body_schema_learner.adapt_body_schema(sensory_data, motor_commands)

    def test_update_kinematic_model_success(self, body_schema_learner):
        # Setup
        body_schema_learner.biomech_constraints.apply_joint_limits.return_value = torch.tensor([0.1, 0.2, 0.3])
        
        # Execute
        result = body_schema_learner.update_kinematic_model([0.1, 0.2, 0.3], [(1.0, 2.0, 3.0)])
        
        # Verify
        assert "kinematic_loss" in result
        assert "updated_joints" in result
        assert result["target_achieved"] is True

    def test_update_kinematic_model_invalid_data(self, body_schema_learner):
        # Execute & Verify
        with pytest.raises(Exception):
            body_schema_learner.update_kinematic_model("invalid", [(1.0, 2.0, 3.0)])

    def test_calibrate_sensorimotor_map_success(self, body_schema_learner):
        # Setup
        calibration_data = {
            'motor_commands': [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
            'sensory_readings': [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        }
        body_schema_learner.physics_constraints.newtonian_mechanics.return_value = True
        body_schema_learner.codonic_layer.predict_sensory_output.return_value = torch.tensor(calibration_data['sensory_readings'])
        
        # Execute
        result = body_schema_learner.calibrate_sensorimotor_map(calibration_data)
        
        # Verify
        assert "calibration_loss" in result
        assert "physics_valid" in result
        assert result["calibration_complete"] is True

    def test_calibrate_sensorimotor_map_missing_key(self, body_schema_learner):
        # Setup
        calibration_data = {
            'motor_commands': [[1.0, 2.0, 3.0]]
            # Missing sensory_readings
        }
        
        # Execute & Verify
        with pytest.raises(ValueError):
            body_schema_learner.calibrate_sensorimotor_map(calibration_data)

    def test_calibrate_sensorimotor_map_mismatched_shapes(self, body_schema_learner):
        # Setup
        calibration_data = {
            'motor_commands': [[1.0, 2.0]],  # Mismatched shapes
            'sensory_readings': [[0.1, 0.2, 0.3]]
        }
        
        # Execute & Verify
        with pytest.raises(ValueError):
            body_schema_learner.calibrate_sensorimotor_map(calibration_data)

    def test_adapt_body_schema_computes_correct_error(self, body_schema_learner):
        # Setup
        sensory_data = torch.randn(10, 3)
        motor_commands = torch.randn(10, 3)
        body_schema_learner.pinn_model.return_value = sensory_data
        
        # Execute
        result = body_schema_learner.adapt_body_schema(sensory_data, motor_commands)
        
        # Verify
        assert isinstance(result["adaptation_error"], float)
        assert result["model_parameters_updated"] is True

    def test_update_kinematic_model_applies_joint_limits(self, body_schema_learner):
        # Setup
        joint_angles = [0.1, 0.2, 0.3]
        target_positions = [(1.0, 2.0, 3.0)]
        constrained_joints = torch.tensor([0.05, 0.1, 0.15])
        body_schema_learner.biomech_constraints.apply_joint_limits.return_value = constrained_joints
        
        # Execute
        result = body_schema_learner.update_kinematic_model(joint_angles, target_positions)
        
        # Verify
        assert result["updated_joints"] == constrained_joints.tolist()

    @patch("src.body_schema_learner.compute_adaptation_gradient")
    @patch("src.body_schema_learner.torch.optim")
    def test_adapt_body_schema_with_mock_gradient(self, mock_optim, mock_gradient, body_schema_learner):
        # Setup
        sensory_data = torch.randn(10, 3)
        motor_commands = torch.randn(10, 3)
        mock_gradient.return_value = torch.randn(10, 3)
        body_schema_learner.pinn_model.return_value = sensory_data
        body_schema_learner.codonic_layer.predict_sensory_output.return_value = sensory_data
        
        # Execute
        result = body_schema_learner.adapt_body_schema(sensory_data, motor_commands)
        
        # Verify
        assert result["model_parameters_updated"] is True

    def test_update_kinematic_model_with_tensor_inputs(self, body_schema_learner):
        # Setup
        joint_angles = torch.tensor([0.1, 0.2, 0.3])
        target_positions = torch.tensor([[1.0, 2.0, 3.0]])
        
        # Execute & Verify
        with pytest.raises(Exception):
            body_schema_learner.update_kinematic_model(joint_angles, target_positions)

    def test_calibrate_sensorimotor_map_validation(self, body_schema_learner):
        # Setup
        calibration_data = {
            'motor_commands': [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
            'sensory_readings': [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        }
        body_schema_learner.physics_constraints.newtonian_mechanics.return_value = True
        body_schema_learner.codonic_layer.predict_sensory_output.return_value = torch.tensor(calibration_data['sensory_readings'])
        
        # Execute
        result = body_schema_learner.calibrate_sensorimotor_map(calibration_data)
        
        # Verify
        assert result["physics_valid"] is True
        assert result["calibration_complete"] is True

    def test_adapt_body_schema_handles_empty_inputs(self, body_schema_learner):
        # Setup
        sensory_data = torch.tensor([])
        motor_commands = torch.tensor([])
        body_schema_learner.pinn_model.return_value = sensory_data
        
        # Execute & Verify
        with pytest.raises(Exception):
            body_schema_learner.adapt_body_schema(sensory_data, motor_commands)

    def test_update_kinematic_model_empty_lists(self, body_schema_learner):
        # Execute & Verify
        with pytest.raises(Exception):
            body_schema_learner.update_kinematic_model([], [])

    def test_calibrate_sensorimotor_map_empty_data(self, body_schema_learner):
        # Setup
        calibration_data = {
            'motor_commands': [],
            'sensory_readings': []
        }
        
        # Execute & Verify
        with pytest.raises(ValueError):
            body_schema_learner.calibrate_sensorimotor_map(calibration_data)