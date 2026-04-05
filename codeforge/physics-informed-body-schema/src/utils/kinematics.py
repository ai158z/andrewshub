import torch
import numpy as np
from typing import Tuple, Union
import logging
from scipy.optimize import minimize
from scipy.spatial.distance import cdist

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def forward_kinematics(joint_angles: Union[torch.Tensor, np.ndarray], 
                     link_lengths: Union[torch.Tensor, np.ndarray]) -> Union[torch.Tensor, np.ndarray]:
    """
    Compute forward kinematics for a kinematic chain.
    
    Args:
        joint_angles: Joint angles in radians, shape (n_joints,) or (batch_size, n_joints)
        link_lengths: Length of each link in the chain, shape (n_joints,)
        
    Returns:
        torch.Tensor or np.ndarray: End-effector positions, shape (batch_size, 2) or (2,)
    """
    # Convert to tensors if numpy arrays
    if isinstance(joint_angles, np.ndarray):
        joint_angles = torch.from_numpy(joint_angles).float()
    if isinstance(link_lengths, np.ndarray):
        link_lengths = torch.from_numpy(link_lengths).float()
    
    # Handle empty inputs
    if joint_angles.numel() == 0 or link_lengths.numel() == 0:
        raise ValueError("Empty input tensors")
    
    # Handle batch dimension
    if len(joint_angles.shape) == 1:
        joint_angles = joint_angles.unsqueeze(0)
        batch_size = 1
    else:
        batch_size = joint_angles.shape[0]
    
    # Expand link_lengths to match batch size
    if len(link_lengths.shape) == 1:
        link_lengths = link_lengths.unsqueeze(0)
    
    # Handle case where we have a single joint configuration but multiple link lengths
    if link_lengths.shape[0] == 1 and batch_size > 1:
        link_lengths = link_lengths.expand(batch_size, -1)
    
    # Compute cumulative angles
    cumulative_angles = torch.cumsum(joint_angles, dim=1)
    
    # Compute x, y positions 
    x_positions = torch.cumsum(torch.cos(cumulative_angles) * link_lengths, dim=1)
    y_positions = torch.cumsum(torch.sin(cumulative_angles) * link_lengths, dim=1)
    
    # Return end-effector position (last link position)
    end_effector_x = x_positions[:, -1:]
    end_effector_y = y_positions[:, -1:]
    
    return torch.cat([end_effector_x, end_effector_y], dim=1)

def inverse_kinematics(target_position: Union[torch.Tensor, np.ndarray, list], 
                     link_lengths: Union[torch.Tensor, np.ndarray, list]) -> torch.Tensor:
    """
    Compute inverse kinematics to find joint angles that achieve target position.
    
    Args:
        target_position: Target (x, y) position, shape (2,) or (batch_size, 2)
        link_lengths: Length of each link in the chain, shape (n_joints,)
        
    Returns:
        torch.Tensor: Joint angles that achieve the target position
    """
    # Convert inputs to appropriate types
    if isinstance(target_position, (list, np.ndarray)):
        target_position = torch.tensor(target_position, dtype=torch.float32)
    if isinstance(link_lengths, (list, np.ndarray)):
        link_lengths = torch.tensor(link_lengths, dtype=torch.float32)
    
    # Ensure 2D tensors
    if len(target_position.shape) == 1:
        target_position = target_position.unsqueeze(0)
    if len(link_lengths.shape) == 1:
        link_lengths = link_lengths.unsqueeze(0)
    
    # Number of joints from link_lengths
    n_joints = link_lengths.shape[-1]
    
    # Handle case where we have batch of targets but single link configuration
    if target_position.shape[0] > 1 and link_lengths.shape[0] == 1:
        # Use expand instead of the boolean expression
        pass
    
    # Use the last target if multiple targets
    if target_position.shape[0] > 1:
        target_position = target_position[-1:].clone()  # Use last target for single solution
    
    # Objective function for optimization
    def ik_objective(joint_angles):
        # Convert to tensor for computation
        joint_angles_tensor = torch.tensor(joint_angles, dtype=torch.float32, requires_grad=True)
        
        # Compute forward kinematics
        end_effector = forward_kinematics(joint_angles_tensor, link_lengths)
        
        # Compute error between target and actual position
        error = torch.norm(end_effector - target_position, dim=-1).mean()
        return error.item()
    
    # Initial guess (all zeros)
    initial_angles = np.zeros(n_joints)
    
    # Optimize using scipy
    result = minimize(ik_objective, initial_angles, method='BFGS')
    
    # Return optimized joint angles
    return torch.tensor(result.x, dtype=torch.float32)