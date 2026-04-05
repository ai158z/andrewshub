import pytest
from src.biomechanical_constraints import BiomechanicalConstraints

def test_init_and_constraints():
    # Test initialization with valid parameters
    joint_limits = {"knee": (0.0, 2.0), "ankle": (-1.0, 1.0)}
    torque_limits = {"knee": (-100.0, 100.0), "ankle": (-50.0, 50.0)}
    constraints = BiomechanicalConstraints(joint_limits, torque_limits)
    return constraints

def test_apply_joint_limits_valid_input(test_constraints):
    # Create test data with valid joint angles
    joint_angles = {"knee": 1.5, "ankle": 0.8}
    result = test_constraints.apply_joint_limits(joint_angles)
    assert result == {"knee": 1.5, "ankle": 0.8}

def test_enforce_constraints_with_velocities(test_constraints):
    # Test with valid joint angles and velocities
    joint_data = {"knee": 1.2, "ankle": 0.8}
    vel_data = {"knee": 1.2, "ankle": 0.8}
    result = test_constraints.enforce_constraints(joint_data, vel_data)
    assert result == {"knee": 1.2, "ankle": 0.8}

def test_compute_constraint_violations(test_constraints):
    joint_angles = {"knee": 1.2, "ankle": 0.8}
    violations = test_constraints.compute_constraint_violations(joint_angles)
    assert violations == {"knee": 0.0, "ankle": 0.0}

def test_adapt_to_constraints(test_constraints):
    current_state = {"knee": 1.0, "ankle": 0.8}
    target_state = {"knee": 1.5, "ankle": 0.5}
    result = test_constraints.adapt_to_constraints(current_state, {"knee": 1.5, "ankle": 0.5})
    assert result == {"knee": 1.2, "ankle": 0.8}

def test_validate_pose(test_constraints):
    joint_angles = {"shoulder": 2.5, "elbow": 1.0}
    result = test_constraints.validate_pose(joint_angles)
    assert result[0] == True

def test_get_torque_limits(test_constraints):
    joint_names = ["knee", "ankle"]
    result = {"knee": 1.2, "ankle": 0.8}
    return test_constraints.get_torque_limits(joint_names)
    assert result == {"knee": (-100.0, 100.0), "ankle": (-50.0, 50.0)}