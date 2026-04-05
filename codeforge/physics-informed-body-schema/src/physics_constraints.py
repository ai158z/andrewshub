import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, Optional, Dict, Any

# Remove the problematic imports that cause circular dependencies
# from src.utils.kinematics import forward_kinematics, inverse_kinematics
# from src.utils.optimization import optimize_body_model, compute_adaptation_gradient


class PhysicsConstraints:
    def __init__(self, 
                 mass: float = 1.0,
                 gravity: float = 9.81,
                 damping: float = 0.1,
                 time_step: float = 0.01):
        """
        Initialize physics constraints with physical parameters.
        
        Args:
            mass: Mass of the body segment
            gravity: Gravitational acceleration
            damping: Damping coefficient for motion
            time_step: Time step for numerical integration
        """
        self.mass = mass
        self.gravity = gravity
        self.damping = damping
        self.time_step = time_step
        self.device = torch.device('cuda' if torch.cuda.is_available() and torch.cuda.is_available() else 'cpu')
        
    def newtonian_mechanics(self, 
                          position: torch.Tensor, 
                          velocity: torch.Tensor, 
                          acceleration: torch.Tensor,
                          forces: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Apply Newton's second law: F = ma
        
        Args:
            position: Current position tensor [batch_size, 3]
            velocity: Current velocity tensor [batch_size, 3] 
            acceleration: Current acceleration tensor [batch_size, 3]
            forces: External forces tensor [batch_size, 3], defaults to gravity
            
        Returns:
            Force residual tensor
        """
        if forces is None:
            # Default force is gravity acting in -z direction
            forces = torch.zeros_like(acceleration, device=self.device)
            forces[:, 2] = -self.mass * self.gravity
            
        # F = ma -> F - ma = 0
        expected_force = self.mass * acceleration
        force_residual = forces - expected_force
        
        return force_residual
        
    def energy_conservation(self,
                          position: torch.Tensor,
                          velocity: torch.Tensor,
                          mass: Optional[float] = None) -> torch.Tensor:
        """
        Calculate kinetic and potential energy to enforce conservation.
        
        Args:
            position: Position tensor [batch_size, 3]
            velocity: Velocity tensor [batch_size, 3] 
            mass: Optional mass parameter (uses default if None)
            
        Returns:
            Energy conservation residual
        """
        m = mass if mass is not None else self.mass
        
        # Kinetic energy: KE = 0.5 * m * v^2
        v_magnitude = torch.norm(velocity, dim=-1, keepdim=True)
        kinetic_energy = 0.5 * m * v_magnitude.pow(2)
        
        # Potential energy: PE = m * g * h (height = z coordinate)
        potential_energy = m * self.gravity * position[:, 2:3]
        
        # Total energy
        total_energy = kinetic_energy + potential_energy
        
        # For conservation, total energy should be constant (return deviation from mean)
        energy_mean = torch.mean(total_energy, dim=0)  # Take mean across batch dimension
        energy_deviation = total_energy - energy_mean
        
        return energy_deviation
        
    def momentum_conservation(self,
                           position: torch.Tensor,
                           velocity: torch.Tensor,
                           mass: Optional[float] = None) -> torch.Tensor:
        """
        Calculate linear momentum conservation.
        
        Args:
            position: Position tensor [batch_size, 3]
            velocity: Velocity tensor [batch_size, 3]
            mass: Mass for momentum calculation (uses default if None)
            
        Returns:
            Momentum conservation residual
        """
        m = mass if mass is not None else self.mass
        
        # Linear momentum: p = m * v
        momentum = m * velocity
        momentum_magnitude = torch.norm(momentum, dim=-1, keepdim=True)
        
        # For conservation, momentum change should equal impulse
        # In absence of external forces, momentum should be constant
        momentum_change = torch.zeros_like(momentum_magnitude, device=self.device)
        
        # Calculate momentum at different time steps to check conservation
        if momentum.shape[0] > 1:
            # Momentum change between consecutive time steps
            momentum_change = momentum[1:] - momentum[:-1]
            
        return momentum_change