import torch
import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np

from src.neural_networks.codonic_network import CodonicNetwork

@pytest.fixture
def codonic_network():
    return CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)

@pytest.fixture
def mock_input():
    return torch.randn(2, 20, 10)  # (batch, seq_len, features)

def test_init_codonic_network():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    assert network.input_size == 10
    assert network.output_size == 5
    assert network.n_lags == 10
    assert network.hidden_size == 64

def test_forward_pass(codonic_network, mock_input):
    with patch.object(codonic_network.pinn_body_model, 'forward') as mock_pinn, \
         patch.object(codonic_network.biomechanical_constraints, 'apply_joint_limits') as mock_constraints, \
         patch.object(codonic_network.physics_constraints, 'newtonian_mechanics') as mock_newton, \
         patch.object(codonic_network.physics_constraints, 'energy_conservation') as mock_energy, \
         patch.object(codonic_network.physics_constraints, 'momentum_conservation') as mock_momentum, \
         patch.object(codonic_network.codonic_layer, 'predict_sensory_output') as mock_codonic, \
         patch.object(codonic_network.codonic_layer, 'integrate_with_pinn') as mock_integrate:
        
        mock_constraints.return_value = mock_input
        mock_pinn.return_value = mock_input
        mock_newton.return_value = mock_input
        mock_energy.return_value = mock_input
        mock_momentum.return_value = mock_input
        mock_codonic.return_value = mock_input
        mock_integrate.return_value = torch.randn(2, 20, 5)
        
        output = codonic_network.forward(mock_input)
        assert output.shape == (2, 20, 5)

def test_predict_sensory_state(codonic_network):
    motor_commands = torch.randn(2, 10)
    with patch.object(codonic_network.rynn_ec_video_analyzer, 'predict_sensory_state') as mock_predict, \
         patch.object(codonic_network.body_schema, 'adapt_body_schema') as mock_adapt, \
         patch.object(codonic_network.body_schema, 'calibrate_sensorimotor_map') as mock_calibrate, \
         patch.object(codonic_network.body_schema, 'update_kinematic_model') as mock_update:
        
        mock_predict.return_value = torch.randn(2, 10)
        mock_adapt.return_value = torch.randn(2, 10)
        mock_calibrate.return_value = torch.randn(2, 10)
        mock_update.return_value = torch.randn(2, 10)
        
        result = codonic_network.predict_sensory_state(motor_commands)
        assert result.shape == (2, 10)

def test_compute_loss(codonic_network):
    predicted = torch.randn(2, 5)
    target = torch.randn(2, 5)
    
    with patch.object(codonic_network.pinn_body_model, 'compute_physics_loss') as mock_physics_loss, \
         patch.object(codonic_network.pinn_body_model, 'boundary_condition_loss') as mock_boundary_loss:
        
        mock_physics_loss.return_value = torch.tensor(0.1)
        mock_boundary_loss.return_value = torch.tensor(0.05)
        
        loss = codonic_network.compute_loss(predicted, target)
        assert isinstance(loss, torch.Tensor)
        assert loss.item() >= 0

def test_biomechanical_constraints_validation(codonic_network, mock_input):
    with patch.object(codonic_network.biomechanical_constraints, 'validate_pose') as mock_validate, \
         patch.object(codonic_network.biomechanical_constraints, 'apply_joint_limits') as mock_limits:
        
        mock_validate.return_value = False  # Simulate invalid pose
        mock_limits.return_value = mock_input
        
        # Test that warning is logged for invalid pose
        with patch('src.neural_networks.codonic_network.logger') as mock_logger:
            codonic_network.forward(mock_input)
            mock_logger.warning.assert_called()

def test_components_are_initialized():
    network = CodonicNetwork(input_size=8, hidden_size=32, output_size=4, n_lags=5)
    assert network.pinn_body_model is not None
    assert network.body_schema is not None
    assert network.codonic_layer is not None
    assert network.physics_constraints is not None
    assert network.biomechanical_constraints is not None
    assert network.rynn_ec_video_analyzer is not None

def test_forward_kinematics_call():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    motor_commands = torch.randn(2, 10)
    
    with patch('src.neural_networks.codonic_network.forward_kinematics') as mock_fk:
        mock_fk.return_value = torch.randn(2, 10)
        # Just ensure it can be called without error
        network.predict_sensory_state(motor_commands)

def test_inverse_kinematics_not_called_in_main_flow():
    # This test ensures we're not accidentally using inverse kinematics in main flow
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    with patch('src.neural_networks.codonic_network.inverse_kinematics') as mock_ik:
        mock_input = torch.randn(2, 20, 10)
        network.forward(mock_input)
        # inverse_kinematics should not be called in forward - it's only used in predict_sensory_state
        mock_ik.assert_not_called()

def test_codonic_layer_integration():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    with patch.object(network.codonic_layer, 'register_codonic_layer') as mock_register, \
         patch.object(network.codonic_layer, 'predict_sensory_output') as mock_predict, \
         patch.object(network.codonic_layer, 'integrate_with_pinn') as mock_integrate:
        
        mock_predict.return_value = torch.randn(2, 20, 5)
        mock_integrate.return_value = torch.randn(2, 20, 5)
        
        mock_input = torch.randn(2, 20, 10)
        result = network.forward(mock_input)
        assert result is not None

def test_pinn_body_model_integration():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    with patch.object(network.pinn_body_model, 'forward') as mock_pinn:
        mock_pinn.return_value = torch.randn(2, 20, 10)
        mock_input = torch.randn(2, 20, 10)
        result = network.forward(mock_input)
        mock_pinn.assert_called()

def test_physics_constraints_chaining():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    with patch.object(network.physics_constraints, 'newtonian_mechanics') as mock_newton, \
         patch.object(network.physics_constraints, 'energy_conservation') as mock_energy, \
         patch.object(network.physics_constraints, 'momentum_conservation') as mock_momentum:
        
        mock_newton.return_value = torch.randn(2, 20, 10)
        mock_energy.return_value = torch.randn(2, 20, 10)
        mock_momentum.return_value = torch.randn(2, 20, 10)
        
        mock_input = torch.randn(2, 20, 10)
        result = network.forward(mock_input)
        mock_newton.assert_called()
        mock_energy.assert_called()
        mock_momentum.assert_called()

def test_body_schema_methods_chaining():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    with patch.object(network.body_schema, 'adapt_body_schema') as mock_adapt, \
         patch.object(network.body_schema, 'calibrate_sensorimotor_map') as mock_calibrate, \
         patch.object(network.body_schema, 'update_kinematic_model') as mock_update:
        
        mock_adapt.return_value = torch.randn(2, 10)
        mock_calibrate.return_value = torch.randn(2, 10)
        mock_update.return_value = torch.randn(2, 10)
        
        motor_commands = torch.randn(2, 10)
        result = network.predict_sensory_state(motor_commands)
        mock_adapt.assert_called()
        mock_calibrate.assert_called()
        mock_update.assert_called()

def test_loss_components():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    predicted = torch.randn(2, 5)
    target = torch.randn(2, 5)
    
    with patch.object(network.pinn_body_model, 'compute_physics_loss') as mock_physics, \
         patch.object(network.pinn_body_model, 'boundary_condition_loss') as mock_boundary:
        
        mock_physics.return_value = torch.tensor(0.1)
        mock_boundary.return_value = torch.tensor(0.05)
        
        loss = network.compute_loss(predicted, target, physics_weight=2.0, boundary_weight=0.5)
        expected_loss = torch.nn.functional.mse_loss(predicted, target) + 2.0 * 0.1 + 0.5 * 0.05
        assert torch.isclose(loss, expected_loss, atol=1e-6)

def test_codonic_layer_registration():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    with patch.object(network.codonic_layer, 'register_codonic_layer') as mock_register:
        # Should be called during initialization
        mock_register.assert_called_once_with(10, 64, 5)

def test_empty_input_handling():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    empty_input = torch.empty(0, 0, 10)
    with pytest.raises((AssertionError, RuntimeError)):
        network.forward(empty_input)

def test_single_sample_input():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    single_sample = torch.randn(1, 1, 10)
    try:
        result = network.forward(single_sample)
        assert result.shape[0] == 1
    except Exception:
        pytest.fail("Forward pass failed for single sample input")

def test_large_input_handling():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    large_input = torch.randn(32, 100, 10)  # Large batch and sequence
    with patch.object(network.pinn_body_model, 'forward') as mock_pinn:
        mock_pinn.return_value = large_input
        result = network.forward(large_input)
        assert result is not None

def test_loss_weights_effect():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    predicted = torch.randn(2, 5)
    target = torch.randn(2, 5)
    
    with patch.object(network.pinn_body_model, 'compute_physics_loss') as mock_physics, \
         patch.object(network.pinn_body_model, 'boundary_condition_loss') as mock_boundary:
        
        mock_physics.return_value = torch.tensor(1.0)
        mock_boundary.return_value = torch.tensor(1.0)
        
        # Test with default weights
        loss1 = network.compute_loss(predicted, target)
        
        # Test with higher weights
        loss2 = network.compute_loss(predicted, target, physics_weight=2.0, boundary_weight=2.0)
        
        # Higher weights should give higher loss
        assert loss2 > loss1

def test_zero_weights_loss():
    network = CodonicNetwork(input_size=10, hidden_size=64, output_size=5, n_lags=10)
    predicted = torch.randn(2, 5)
    target = torch.randn(2, 5)
    
    with patch.object(network.pinn_body_model, 'compute_physics_loss') as mock_physics, \
         patch.object(network.pinn_body_model, 'boundary_condition_loss') as mock_boundary:
        
        mock_physics.return_value = torch.tensor(0.0)
        mock_boundary.return_value = torch.tensor(0.0)
        
        # With zero additional losses, should equal base MSE
        base_loss = torch.nn.functional.mse_loss(predicted, target)
        total_loss = network.compute_loss(predicted, target, physics_weight=0.0, boundary_weight=0.0)
        assert torch.isclose(base_loss, total_loss, atol=1e-6)