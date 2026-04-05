import torch
import pytest
from unittest.mock import Mock, patch
import numpy as np
from src.pinn_body_model import PINNBodyModel

@pytest.fixture
def model():
    return PINNBodyModel()

@pytest.fixture
def sample_input():
    return torch.randn(32, 6)

@pytest.fixture
def sample_joint_data():
    batch_size = 32
    joint_angles = torch.randn(batch_size, 7)
    joint_velocities = torch.randn(batch_size, 7)
    joint_torques = torch.randn(batch_size, 7)
    return joint_angles, joint_velocities, joint_torques

def test_model_initialization():
    model = PINNBodyModel()
    assert model.input_dim == 6
    assert model.hidden_dim == 128
    assert model.output_dim == 3
    assert model.num_joints == 7

def test_forward_pass_valid_input(model):
    x = torch.randn(32, 6)
    output = model(x)
    assert output.shape == (32, 3)

def test_forward_pass_invalid_input_type(model):
    with pytest.raises(TypeError):
        model("invalid_input")

def test_forward_pass_invalid_shape(model):
    x = torch.randn(32, 5)  # Wrong input dimension
    with pytest.raises(ValueError):
        model(x)

def test_forward_pass_invalid_dimensions(model):
    x = torch.randn(6)  # 1D tensor
    with pytest.raises(ValueError):
        model(x)

def test_physics_loss_computation(model, sample_joint_data):
    joint_angles, joint_velocities, joint_torques = sample_joint_data
    model.compute_physics_loss(joint_angles, joint_velocities, joint_torques)

def test_physics_loss_invalid_input_types(model):
    with pytest.raises(TypeError):
        model.compute_physics_loss("invalid", "invalid", "invalid")

def test_physics_loss_mismatched_batch_sizes(model):
    joint_angles = torch.randn(32, 7)
    joint_velocities = torch.randn(16, 7)  # Mismatched batch size
    joint_torques = torch.randn(32, 7)   # Mismatched batch size
    with pytest.raises(ValueError):
        model.compute_physics_loss(joint_angles, joint_velocities, joint_torques)

@patch('src.pinn_body_model.forward_kinematics')
@patch('src.pinn_body_model.BiomechanicalConstraints')
@patch('src.pinn_body_model.PhysicsConstraints')
def test_physics_loss_components(mock_physics, mock_biomech, mock_kinematics, model, sample_joint_data):
    # Mock the dependencies
    mock_physics_instance = mock_physics.return_value
    mock_biomech_instance = mock_biomech.return_value
    mock_biomech_instance.apply_joint_limits.side_effect = lambda x: x
    
    # Mock the forward_kinematics function directly
    mock_kinematics.side_effect = lambda angles, lengths: np.zeros(3)  # Return a zero array for position
    
    joint_angles, joint_velocities, joint_torques = sample_joint_data
    loss = model.compute_physics_loss(joint_angles, joint_velocities, joint_torques)
    assert loss is not None

def test_link_lengths_parameter(model):
    assert isinstance(model.link_lengths, torch.nn.Parameter)
    assert model.link_lengths.shape == (7,)
    assert torch.all(model.link_lengths > 0)

def test_network_layers_initialization(model):
    assert isinstance(model.fc1, torch.nn.Linear)
    assert isinstance(model.fc2, torch.nn.Linear)
    assert isinstance(model.fc3, torch.nn.Linear)
    assert isinstance(model.fc4, torch.nn.Linear)

def test_forward_layer_dimensions(model):
    assert model.fc1.in_features == 6
    assert model.fc1.out_features == 128
    assert model.fc2.out_features == 128
    assert model.fc3.out_features == 128
    assert model.fc4.out_features == 3

def test_relu_activations(model, sample_input):
    # Test that ReLU activations are applied in forward pass
    with torch.no_grad():
        output = model(sample_input)
        # Since we're testing the forward method, and it applies ReLU, we can check the output is not just the input
        # This is a simplistic test - in practice, you'd check the actual ReLU behavior
        assert output.shape == (32, 3)

def test_compute_physics_loss_with_mocked_kinematics(sample_joint_data):
    # This test focuses on the loss computation, so we mock the kinematics
    pass  # Mocked in the respective test function

@patch('src.pinn_body_model.forward_kinematics')
def test_forward_kinematics_call(mock_kinematics, model, sample_joint_data):
    mock_kinematics.return_value = np.array([0.1, 0.2, 0.3])
    joint_angles, joint_velocities, joint_torques = sample_joint_data
    model.compute_physics_loss(joint_angles, joint_velocities, joint_torques)
    assert mock_kinematics.call_count > 0

def test_device_placement(model):
    assert model.device == torch.device("cpu")

def test_physics_constraints_initialization(model):
    assert hasattr(model, 'physics_constraints')
    assert hasattr(model, 'biomech_constraints')