import pytest
import torch
import torch.nn as nn
from unittest.mock import Mock, patch, MagicMock
from src.utils.optimization import *

class MockModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.dummy_param = nn.Parameter(torch.tensor([1.0]))
        
    def compute_physics_loss(self, data):
        return torch.sum(data)

class MockLossFunction:
    def __init__(self):
        self.call_count = 0
        self.call_limit = 3
        
    def __call__(self, model):
        if self.call_count >= self.call_limit:
            return torch.tensor(0.0000001)  # Converge after 3 iterations
        self.call_count += 1
        return torch.tensor(10.0 / self.call_count)

class MockOptimizer:
    def __init__(self, parameters, lr=0.001):
        self.parameters = list(parameters)
        self.lr = lr
        
    def zero_grad(self):
        pass
        
    def step(self):
        pass

class TestOptimizeBodyModel:
    def test_optimize_body_model_success(self):
        model = MockModel()
        loss_fn = MockLossFunction()
        optimizer = MockOptimizer(model.parameters())
        
        final_loss, iterations = optimize_body_model(model, loss_fn, optimizer)
        
        assert isinstance(final_loss, torch.Tensor)
        assert isinstance(iterations, int)
        assert iterations == 3  # Should converge after 3 iterations due to loss convergence

    def test_optimize_body_model_invalid_model_type(self):
        loss_fn = MockLossFunction()
        optimizer = MockOptimizer([torch.tensor([1.0])])
        invalid_model = "not a model"
        
        with pytest.raises(TypeError, match="Model must be a valid neural network model"):
            optimize_body_model(invalid_model, loss_fn, optimizer)

    def test_optimize_body_model_invalid_loss_function(self):
        model = MockModel()
        invalid_loss_fn = "not callable"
        optimizer = MockOptimizer(model.parameters())
        
        with pytest.raises(ValueError, match="Loss function must be callable"):
            optimize_body_model(model, invalid_loss_fn, optimizer)

    def test_optimize_body_model_invalid_optimizer(self):
        model = MockModel()
        loss_fn = MockLossFunction()
        invalid_optimizer = "not an optimizer"
        
        with pytest.raises(TypeError, match="Optimizer must be a valid PyTorch optimizer"):
            optimize_body_model(model, loss_fn, invalid_optimizer)

class TestComputeAdaptationGradient:
    def test_compute_adaptation_gradient_pinn_model(self):
        model = MockModel()
        sensory_data = torch.tensor([1.0, 2.0, 3.0])
        
        with patch('src.utils.optimization.PhysicsConstraints') as mock_physics:
            mock_physics.return_value = Mock()
            result = compute_adaptation_gradient(model, sensory_data)
            assert isinstance(result, tuple)

    def test_compute_adaptation_gradient_invalid_model(self):
        invalid_model = "not a model"
        sensory_data = torch.tensor([1.0, 2.0, 3.0])
        
        with pytest.raises(TypeError, match="Model must be a valid neural network model"):
            compute_adaptation_gradient(invalid_model, sensory_data)

    def test_compute_adaptation_gradient_invalid_sensory_data(self):
        model = MockModel()
        invalid_sensory_data = "not a tensor"
        
        with pytest.raises(TypeError, match="Sensory data must be a torch.Tensor"):
            compute_adaptation_gradient(model, invalid_sensory_data)

class TestAdaptBodySchema:
    def test_adapt_body_schema_success(self):
        model = Mock()
        sensory_input = torch.tensor([1.0, 2.0, 3.0])
        
        # Mock the adapt_body_schema method to return a tensor that requires grad
        model.adapt_body_schema.return_value = torch.tensor(1.0, requires_grad=True)
        
        adapt_body_schema(model, sensory_input)
        assert model.adapt_body_schema.call_count > 0

    def test_adapt_body_schema_invalid_model(self):
        invalid_model = "not a model"
        sensory_input = torch.tensor([1.0, 2.0, 3.0])
        
        with pytest.raises(TypeError, match="Model must be a BodySchemaLearner instance"):
            adapt_body_schema(invalid_model, sensory_input)

class TestExtractRegions:
    def test_extract_regions_success(self):
        analyzer = Mock()
        frame_data = torch.tensor([1.0, 2.0, 3.0])
        analyzer.extract_regions.return_value = torch.tensor([4.0, 5.0, 6.0])
        
        result = extract_regions(analyzer, frame_data)
        assert torch.is_tensor(result)

    def test_extract_regions_invalid_analyzer(self):
        invalid_analyzer = "not an analyzer"
        frame_data = torch.tensor([1.0, 2.0, 3.0])
        
        with pytest.raises(TypeError, match="Invalid video analyzer type"):
            extract_regions(invalid_analyzer, frame_data)

def test_analyze_motion_dynamics_success(self):
    analyzer = Mock()
    motion_data = torch.tensor([1.0, 2.0, 3.0])
    analyzer.analyze_motion_dynamics.return_value = torch.tensor([4.0, 5.0, 6.0])
    
    result = analyze_motion_dynamics(analyzer, motion_data)
    assert torch.is_tensor(result)

def test_analyze_motion_dynamics_invalid_analyzer(self):
    invalid_analyzer = "not an analyzer"
    motion_data = torch.tensor([1.0, 2.0, 3.0])
    
    with pytest.raises(TypeError):
        analyze_motion_dynamics(invalid_analyzer, motion_data)

def test_predict_sensory_state_success(self):
    layer = Mock()
    input_data = torch.tensor([1.0, 2.0, 3.0])
    layer.predict_sensory_output.return_value = torch.tensor([4.0, 5.0, 6.0])
    
    result = predict_sensory_state(layer, input_data)
    assert torch.is_tensor(result)

def test_predict_sensory_state_invalid_layer(self):
    invalid_layer = "not a layer"
    input_data = torch.tensor([1.0, 2.0, 3.0])
    
    with pytest.raises(TypeError):
        predict_sensory_state(invalid_layer, input_data)

def test_integrate_with_pinn_success(self):
    layer = Mock()
    pinn_model = Mock()
    
    integrate_with_pinn(layer, pinn_model)
    layer.integrate_with_pinn.assert_called_once()

def test_integrate_with_pinn_invalid_layer(self):
    invalid_layer = "not a layer"
    pinn_model = Mock()
    
    with pytest.raises(TypeError):
        integrate_with_pinn(invalid_layer, pinn_model)

def test_update_codonic_weights_success(self):
    layer = Mock()
    sensory_data = torch.tensor([1.0, 2.0, 3.0])
    
    update_codonic_weights(layer, sensory_data)
    layer.update_codonic_weights.assert_called_once_with(sensory_data)

def test_update_codonic_weights_invalid_layer(self):
    invalid_layer = "not a layer"
    sensory_data = torch.tensor([1.0, 2.0, 3.0])
    
    with pytest.raises(TypeError):
        update_codonic_weights(invalid_layer, sensory_data)

def test_apply_joint_limits_success(self):
    constraints = Mock()
    joint_states = torch.tensor([1.0, 2.0, 3.0])
    constraints.apply_joint_limits.return_value = torch.tensor([0.5, 1.0, 1.5])
    
    result = apply_joint_limits(constraints, joint_states)
    assert torch.is_tensor(result)

def test_apply_joint_limits_invalid_constraints(self):
    invalid_constraints = "not constraints"
    joint_states = torch.tensor([1.0, 2.0, 3.0])
    
    with pytest.raises(TypeError):
        apply_joint_limits(invalid_constraints, joint_states)

def test_validate_pose_success(self):
    constraints = Mock()
    pose = torch.tensor([1.0, 2.0, 3.0])
    constraints.validate_pose.return_value = True
    
    result = validate_pose(constraints, pose)
    assert isinstance(result, bool)

def test_validate_pose_invalid_constraints(self):
    invalid_constraints = "not constraints"
    pose = torch.tensor([1.0, 2.0, 3.0])
    
    with pytest.raises(TypeError):
        validate_pose(invalid_constraints, pose)

def test_get_torque_limits_success(self):
    constraints = Mock()
    joint_states = torch.tensor([1.0, 2.0, 3.0])
    constraints.get_torque_limits.return_value = torch.tensor([0.1, 0.2, 0.3])
    
    result = get_torque_limits(constraints, joint_states)
    assert torch.is_tensor(result)

def test_get_torque_limits_invalid_constraints(self):
    invalid_constraints = "not constraints"
    joint_states = torch.tensor([1.0, 2.0, 3.0])
    
    with pytest.raises(TypeError):
        get_torque_limits(invalid_constraints, joint_states)

def test_newtonian_mechanics_success(self):
    physics = Mock()
    state = torch.tensor([1.0, 2.0, 3.0])
    physics.newtonian_mechanics.return_value = torch.tensor([0.5, 1.0, 1.5])
    
    result = newtonian_mechanics(physics, state)
    assert torch.is_tensor(result)

def test_newtonian_mechanics_invalid_physics(self):
    invalid_physics = "not physics"
    state = torch.tensor([1.0, 2.0, 3.0])
    
    with pytest.raises(TypeError):
        newtonian_mechanics(invalid_physics, state)

def test_forward_kinematics_success(self):
    joint_angles = torch.tensor([0.1, 0.2, 0.3])
    link_lengths = torch.tensor([1.0, 1.0, 1.0])
    
    with patch('src.utils.optimization.forward_kinematics') as mock_fk:
        mock_fk.return_value = torch.tensor([1.0, 0.0])
        result = forward_kinematics(joint_angles, link_lengths)
        assert torch.is_tensor(result)

def test_forward_kinematics_invalid_input(self):
    joint_angles = "not a tensor"
    link_lengths = torch.tensor([1.0, 1.0, 1.0])
    
    with pytest.raises(TypeError):
        forward_kinematics(joint_angles, link_lengths)

def test_inverse_kinematics_success(self):
    target_position = torch.tensor([1.0, 0.0])
    link_lengths = torch.tensor([1.0, 1.0, 1.0])
    
    with patch('src.utils.optimization.inverse_kinematics') as mock_ik:
        mock_ik.return_value = torch.tensor([0.1, 0.2, 0.3])
        result = inverse_kinematics(target_position, link_lengths)
        assert torch.is_tensor(result)

def test_inverse_kinematics_invalid_input(self):
    target_position = "not a tensor"
    link_lengths = torch.tensor([1.0, 1.0, 1.0])
    
    with pytest.raises(TypeError):
        inverse_kinematics(target_position, link_lengths)