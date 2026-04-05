import torch
import pytest
import numpy as np
from src.biomechanical_constraints import BiomechanicalConstraints

@pytest.fixture
def constraints():
    return BiomechanicalConstraints()

@pytest.fixture
def sample_limits():
    return {
        'hip_flexion': (-1.5, 1.5),
        'hip_abduction': (-0.5, 0.5),
        'hip_rotation': (-0.8, 0.8),
        'knee_angle': (-2.8, 0.0),
        'ankle_angle': (-0.9, 0.9)
    }

def test_apply_joint_limits(constraints):
    # Test with joints exceeding limits
    test_data = torch.tensor([2.0, -1.5, 4.0, 0.5, -3.0, 1.0])
    limited_data = constraints.apply_joint_limits(test_data)
    
    # Check that all values are within reasonable joint limits
    assert torch.all(limited_data >= -torch.pi)
    assert torch.all(limited_data <= torch.pi)
    
    # Test with valid joint angles that should not be modified
    valid_data = torch.tensor([0.5, -0.3, 1.2, 0.1, -0.8, 0.4])
    limited_valid = constraints.apply_joint_limits(valid_data)
    assert torch.allclose(valid_data, limited_valid, atol=1e-6)

def test_validate_pose_valid(constraints):
    # Test valid pose
    valid_pose = torch.tensor([0.1, -0.2, 0.3, -0.1, 0.25, -0.15])
    assert constraints.validate_pose(valid_pose) is True

def test_validate_pose_invalid(constraints):
    # Test invalid pose (exceeding joint limits)
    invalid_pose = torch.tensor([4.0, -3.5, 3.2, 0.1, -3.5, 1.0])
    assert constraints.validate_pose(invalid_pose) is False

def test_validate_pose_boundary(constraints):
    # Test edge case at boundary
    boundary_pose = torch.tensor([torch.pi, -torch.pi, torch.pi, -0.1, 0.2, -0.3])
    assert constraints.validate_pose(boundary_pose) is True

def test_check_torque_limits_within(constraints):
    # Test torque within limits
    torques_within = torch.tensor([10.0, 15.0, 8.0, 12.0, 5.0])
    limits = constraints.get_torque_limits()
    assert constraints.check_torque_limits(torques_within, limits) is True

def test_check_torque_limits_exceed(constraints):
    # Test torque exceeding limits
    torques_exceed = torch.tensor([35.0, 45.0, 25.0, 10.0, 50.0])
    limits = constraints.get_torque_limits()
    assert constraints.check_torque_limits(torques_exceed, limits) is False

def test_check_torque_limits_mixed(constraints):
    # Test with mixed torques
    mixed_torques = torch.tensor([20.0, 60.0, 15.0, 5.0, 25.0])
    limits = constraints.get_torque_limits()
    assert constraints.check_torque_limits(mixed_torques, limits) is False

def test_apply_joint_limits_clamps_values(constraints):
    # Test that values are properly clamped
    test_data = torch.tensor([2.0, -1.5, 4.0, 0.5, -3.0, 1.0])
    limited_data = constraints.apply_joint_limits(test_data)
    
    # Values should be clamped to [-pi, pi]
    assert torch.all(limited_data >= -torch.pi)
    assert torch.all(limited_data <= torch.pi)
    
    # Check that values outside limits were actually clamped
    assert not torch.allclose(test_data, limited_data, atol=1e-6)

def test_apply_joint_limits_no_change_for_valid(constraints):
    # Test that valid values are not modified
    valid_data = torch.tensor([0.5, -0.3, 1.2, 0.1, -0.8, 0.4])
    limited_valid = constraints.apply_joint_limits(valid_data)
    assert torch.allclose(valid_data, limited_valid, atol=1e-6)

def test_get_torque_limits_returns_dict(constraints):
    limits = constraints.get_torque_limits()
    assert isinstance(limits, dict)
    assert len(limits) > 0

def test_validate_pose_empty_tensor(constraints):
    empty_pose = torch.tensor([])
    assert constraints.validate_pose(empty_pose) is False

def test_validate_pose_single_value(constraints):
    single_pose = torch.tensor([0.0])
    assert constraints.validate_pose(single_pose) is True

def test_validate_pose_all_zeros(constraints):
    zero_pose = torch.zeros(6)
    assert constraints.validate_pose(zero_pose) is True

def test_apply_joint_limits_extreme_values(constraints):
    # Test with extreme values that need clamping
    extreme_data = torch.tensor([10.0, -10.0, 10.0, -10.0, 10.0, -10.0])
    limited_data = constraints.apply_joint_limits(extreme_data)
    
    # Should be clamped to [-pi, pi]
    assert torch.all(limited_data >= -torch.pi)
    assert torch.all(limited_data <= torch.pi)
    assert not torch.allclose(extreme_data, limited_data, atol=1e-6)

def test_torque_limits_edge_case(constraints):
    # Test torques at exactly the limit values
    limits = constraints.get_torque_limits()
    # Create torques at the exact limit values
    limit_values = torch.tensor([limit[1] for limit in limits.values()])
    assert constraints.check_torque_limits(limit_values, limits) is True

def test_apply_joint_limits_nan(constraints):
    nan_data = torch.tensor([float('nan'), float('nan')])
    with pytest.raises(ValueError):
        constraints.apply_joint_limits(nan_data)

def test_apply_joint_limits_inf(constraints):
    inf_data = torch.tensor([float('inf'), float('-inf')])
    limited_data = constraints.apply_joint_limits(inf_data)
    # inf values should be clamped to finite range
    assert torch.all(torch.isfinite(limited_data))
    assert torch.all(limited_data >= -torch.pi)
    assert torch.all(limited_data <= torch.pi)

def test_validate_pose_nan(constraints):
    nan_pose = torch.tensor([float('nan'), float('nan')])
    with pytest.raises(Exception):
        constraints.validate_pose(nan_pose)

def test_validate_pose_inf(constraints):
    inf_pose = torch.tensor([float('inf'), float('-inf')])
    assert constraints.validate_pose(inf_pose) is False