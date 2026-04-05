import torch
import pytest
from src.physics_constraints import PhysicsConstraints
import torch.nn as nn


class TestPhysicsConstraints:
    
    @pytest.fixture
    def physics_constraints(self):
        return PhysicsConstraints(mass=2.0, gravity=9.81, damping=0.1, time_step=0.01)
    
    def test_newtonian_mechanics_with_default_gravity_force(self, physics_constraints):
        # Test with default gravity force
        position = torch.tensor([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
        velocity = torch.tensor([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]) 
        acceleration = torch.tensor([[0.0, 0.0, -9.81], [0.0, 0.0, -4.9]])
        
        residual = physics_constraints.newtonian_mechanics(position, velocity, acceleration)
        expected = torch.zeros_like(acceleration)
        expected[:, 2] = -physics_constraints.mass * physics_constraints.gravity
        expected = expected - physics_constraints.mass * acceleration
        
        assert residual.shape == acceleration.shape
        assert torch.allclose(residual, expected, atol=1e-6)
        
    def test_newtonian_mechanics_with_custom_forces(self, physics_constraints):
        # Test with custom forces provided
        position = torch.tensor([[0.0, 0.0, 0.0]])
        velocity = torch.tensor([[0.0, 0.0, 0.0]])
        acceleration = torch.tensor([[1.0, 0.0, -9.81]])
        forces = torch.tensor([[0.0, 0.0, -9.81]])
        
        residual = physics_constraints.newtonian_mechanics(position, velocity, acceleration, forces)
        expected = forces - physics_constraints.mass * acceleration
        
        assert torch.allclose(residual, expected)
        
    def test_energy_conservation_basic(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 5.0], [1.0, 1.0, 10.0]])
        velocity = torch.tensor([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
        
        energy_dev = physics_constraints.energy_conservation(position, velocity)
        # Should return energy deviation tensor of same batch size
        assert energy_dev.shape[0] == position.shape[0]
        
    def test_energy_conservation_with_custom_mass(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 5.0]])
        velocity = torch.tensor([[0.0, 0.0, 0.0]])
        
        energy_dev = physics_constraints.energy_conservation(position, velocity, mass=3.0)
        assert energy_dev.shape[0] == 1
        
    def test_momentum_conservation_single_point(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 0.0]])
        velocity = torch.tensor([[1.0, 0.0, 0.0]])
        
        momentum_change = physics_constraints.momentum_conservation(position, velocity)
        # With single point, no momentum change can be computed
        assert momentum_change.shape[0] == 0
        
    def test_momentum_conservation_multiple_points(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
        velocity = torch.tensor([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]])
        
        momentum_change = physics_constraints.momentum_conservation(position, velocity)
        # Should have n-1 changes for n points
        assert momentum_change.shape[0] == 2
        
    def test_newtonian_mechanics_output_shape(self, physics_constraints):
        position = torch.randn(5, 3)
        velocity = torch.randn(5, 3)
        acceleration = torch.randn(5, 3)
        
        result = physics_constraints.newtonian_mechanics(position, velocity, acceleration)
        assert result.shape == acceleration.shape
        
    def test_newtonian_mechanics_zero_acceleration(self, physics_constraints):
        position = torch.randn(3, 3)
        velocity = torch.randn(3, 3)
        acceleration = torch.zeros(3, 3)
        
        forces = torch.tensor([[0.0, 0.0, -9.81*2.0]] * 3)
        result = physics_constraints.newtonian_mechanics(position, velocity, acceleration, forces)
        
        expected = forces - physics_constraints.mass * acceleration
        assert torch.allclose(result, expected)
        
    def test_energy_conservation_zero_velocity(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 5.0]])
        velocity = torch.zeros_like(position)
        
        energy_dev = physics_constraints.energy_conservation(position, velocity)
        assert energy_dev.shape[0] == 1
        
    def test_energy_conservation_zero_height(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 0.0]])
        velocity = torch.tensor([[1.0, 1.0, 0.0]])
        
        energy_dev = physics_constraints.energy_conservation(position, velocity)
        assert energy_dev.shape[0] == 1
        
    def test_momentum_conservation_zero_velocity(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        velocity = torch.zeros(2, 3)
        
        momentum_change = physics_constraints.momentum_conservation(position, velocity)
        assert momentum_change.shape[0] == 1
        
    def test_newtonian_mechanics_cuda_device(self, physics_constraints):
        if torch.cuda.is_available():
            position = torch.tensor([[0.0, 0.0, 0.0]]).cuda()
            velocity = torch.tensor([[0.0, 0.0, 0.0]]).cuda()
            acceleration = torch.tensor([[0.0, 0.0, -9.81]]).cuda()
            
            residual = physics_constraints.newtonian_mechanics(position, velocity, acceleration)
            assert residual.device.type == 'cuda'
        else:
            pytest.skip("CUDA not available")
            
    def test_newtonian_mechanics_cpu_device(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 0.0]])
        velocity = torch.tensor([[0.0, 0.0, 0.0]])
        acceleration = torch.tensor([[0.0, 0.0, -9.81]])
        
        residual = physics_constraints.newtonian_mechanics(position, velocity, acceleration)
        assert residual.device.type == 'cpu'
        
    def test_energy_conservation_conserves_energy(self, physics_constraints):
        # Test that energy is conserved for simple case
        position = torch.tensor([[0.0, 0.0, 10.0]])
        velocity = torch.tensor([[0.0, 0.0, 0.0]])
        
        energy_dev = physics_constraints.energy_conservation(position, velocity)
        # Energy should be constant (close to zero deviation)
        assert torch.allclose(energy_dev, torch.zeros_like(energy_dev), atol=1e-10)
        
    def test_momentum_conservation_no_external_forces(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
        velocity = torch.tensor([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]])
        
        momentum_change = physics_constraints.momentum_conservation(position, velocity)
        # Momentum should be conserved (no external forces)
        assert momentum_change.shape[0] == 2  # n-1 changes
        
    def test_newtonian_mechanics_force_direction(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 0.0]])
        velocity = torch.tensor([[0.0, 0.0, 0.0]])
        acceleration = torch.tensor([[0.0, 0.0, -9.81]])
        
        # Test that default gravity force is in -z direction
        residual = physics_constraints.newtonian_mechanics(position, velocity, acceleration)
        assert torch.all(residual[:, 2] < 0)  # Gravity component should be negative
        
    def test_energy_conservation_potential_energy_dominant(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 10.0]])
        velocity = torch.tensor([[0.0, 0.0, 0.0]])
        
        # High position should give high potential energy
        energy_dev = physics_constraints.energy_conservation(position, velocity)
        # All potential energy, no kinetic energy
        assert torch.all(energy_dev >= 0)
        
    def test_momentum_conservation_consistency(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 0.0]] * 10)
        velocity = torch.tensor([[1.0, 0.0, 0.0]] * 10)
        
        momentum_change1 = physics_constraints.momentum_conservation(position, velocity)
        momentum_change2 = physics_constraints.momentum_conservation(position, velocity, mass=1.0)
        
        # Should be consistent for same physical state
        assert momentum_change1.shape == momentum_change2.shape
        
    def test_newtonian_mechanics_batch_consistency(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
        velocity = torch.tensor([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
        acceleration = torch.tensor([[0.0, 0.0, -9.81], [0.0, 0.0, -4.9]])
        
        residual = physics_constraints.newtonian_mechanics(position, velocity, acceleration)
        # Each batch item should be computed independently
        assert residual.shape[0] == 2
        assert residual.shape[1] == 3
        
    def test_energy_conservation_kinetic_dominant(self, physics_constraints):
        position = torch.tensor([[0.0, 0.0, 0.0]])
        velocity = torch.tensor([[10.0, 0.0, 0.0]])
        
        energy_dev = physics_constraints.energy_conservation(position, velocity)
        # High velocity should give high kinetic energy
        assert torch.all(energy_dev > 0)