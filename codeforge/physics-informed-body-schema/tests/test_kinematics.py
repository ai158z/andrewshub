import torch
import numpy as np
import pytest
from src.utils.kinematics import forward_kinematics, inverse_kinematics

def test_forward_kinematics_single_joint_single_batch():
    joint_angles = torch.tensor([0.0])
    link_lengths = torch.tensor([1.0])
    result = forward_kinematics(joint_angles, link_lengths)
    expected = torch.tensor([[1.0, 0.0]])
    assert torch.allclose(result, expected, atol=1e-6)

def test_forward_kinematics_multiple_joints():
    joint_angles = torch.tensor([0.0, 0.0])
    link_lengths = torch.tensor([1.0, 1.0])
    result = forward_kinematics(joint_angles, link_lengths)
    expected = torch.tensor([[2.0, 0.0]])
    assert result.shape == (1, 2)
    assert torch.allclose(result, expected, atol=1e-6)

def test_forward_kinematics_batch_input():
    joint_angles = torch.tensor([[0.0, 0.0], [np.pi/2, 0.0]])
    link_lengths = torch.tensor([1.0, 1.0])
    result = forward_kinematics(joint_angles, link_lengths)
    assert result.shape == (2, 2)

def test_forward_kinematics_numpy_input():
    joint_angles = np.array([0.0, 0.0])
    link_lengths = np.array([1.0, 1.0])
    result = forward_kinematics(joint_angles, link_lengths)
    assert isinstance(result, torch.Tensor)
    assert result.shape == (1, 2)

def test_forward_kinematics_zero_joints():
    joint_angles = torch.tensor([]).reshape(0, 1)
    link_lengths = torch.tensor([])
    with pytest.raises(RuntimeError):
        forward_kinematics(joint_angles, link_lengths)

def test_forward_kinematics_single_batch_numpy():
    joint_angles = np.array([0.0, 0.0])
    link_lengths = np.array([1.0, 1.0])
    result = forward_kinematics(joint_angles, link_lengths)
    assert result.shape == (1, 2)

def test_inverse_kinematics_single_target():
    target = torch.tensor([2.0, 0.0])
    link_lengths = torch.tensor([1.0, 1.0])
    result = inverse_kinematics(target, link_lengths)
    assert result.shape == (2,)
    assert torch.isfinite(result).all()

def test_inverse_kinematics_list_input():
    target = [2.0, 0.0]
    link_lengths = [1.0, 1.0]
    result = inverse_kinematics(target, link_lengths)
    assert result.shape == (2,)

def test_inverse_kinematics_numpy_input():
    target = np.array([2.0, 0.0])
    link_lengths = np.array([1.0, 1.0])
    result = inverse_kinematics(target, link_lengths)
    assert result.shape == (2,)

def test_inverse_kinematics_list_target_tensor_links():
    target = [1.5, 0.5]
    link_lengths = torch.tensor([1.0, 1.0])
    result = inverse_kinematics(target, link_lengths)
    assert result.shape == (2,)

def test_inverse_kinematics_batch_target():
    target = torch.tensor([[2.0, 0.0]])
    link_lengths = torch.tensor([1.0, 1.0])
    result = inverse_kinematics(target, link_lengths)
    assert result.shape == (2,)

def test_forward_kinematics_zero_angle():
    joint_angles = torch.tensor([0.0, 0.0])
    link_lengths = torch.tensor([1.0, 1.0])
    result = forward_kinematics(joint_angles, link_lengths)
    expected = torch.tensor([[2.0, 0.0]])
    assert torch.allclose(result, expected, atol=1e-6)

def test_forward_kinematics_pi_angle():
    joint_angles = torch.tensor([np.pi, 0.0])
    link_lengths = torch.tensor([1.0, 1.0])
    result = forward_kinematics(joint_angles, link_lengths)
    expected = torch.tensor([[-2.0, 0.0]])
    assert torch.allclose(result, expected, atol=1e-6)

def test_forward_kinematics_right_angle():
    joint_angles = torch.tensor([0.0, np.pi/2])
    link_lengths = torch.tensor([1.0, 1.0])
    result = forward_kinematics(joint_angles, link_lengths)
    expected = torch.tensor([[1.0, 1.0]])
    assert torch.allclose(result, expected, atol=1e-6)

def test_forward_kinematics_batch():
    joint_angles = torch.tensor([[0.0, 0.0], [0.0, np.pi/2]])
    link_lengths = torch.tensor([1.0, 1.0])
    result = forward_kinematics(joint_angles, link_lengths)
    expected = torch.tensor([[[2.0, 0.0]], [[1.0, 1.0]]])
    assert result.shape == (2, 2)

def test_inverse_kinematics_impossible_target():
    target = torch.tensor([5.0, 0.0])  # Unreachable with link lengths [1.0, 1.0]
    link_lengths = torch.tensor([1.0, 1.0])
    result = inverse_kinematics(target, link_lengths)
    assert result.shape == (2,)

def test_forward_kinematics_single_joint_as_batch():
    joint_angles = torch.tensor([[0.0]])
    link_lengths = torch.tensor([1.0])
    result = forward_kinematics(joint_angles, link_lengths)
    expected = torch.tensor([[1.0, 0.0]])
    assert torch.allclose(result, expected, atol=1e-6)

def test_forward_kinematics_empty_inputs():
    joint_angles = torch.tensor([])
    link_lengths = torch.tensor([])
    with pytest.raises(Exception):
        forward_kinematics(joint_angles, link_lengths)

def test_inverse_kinematics_reaches_target():
    target = torch.tensor([1.5, 0.0])
    link_lengths = torch.tensor([1.0, 1.0])
    angles = inverse_kinematics(target, link_lengths)
    pos = forward_kinematics(angles, link_lengths)
    expected_target = torch.tensor([[1.5, 0.0]])
    assert torch.allclose(pos, expected_target, atol=0.1)  # Allow some error for numerical precision

def test_inverse_kinematics_single_target_tensor_links():
    target = torch.tensor([1.5, 0.0])
    link_lengths = torch.tensor([1.0, 1.0])
    result = inverse_kinematics(target, link_lengths)
    assert result.shape == (2,)