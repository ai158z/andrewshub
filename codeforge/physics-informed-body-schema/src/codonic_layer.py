import torch
import torch.nn as nn
import torch.optim as optim
import logging
from typing import Tuple, Optional, Dict, Any
import numpy as np

from src.biomechanical_constraints import BiomechanicalConstraints
from src.body_schema_learner import BodySchemaLearner
from src.rynnec_video_analyzer import RynnECVideoAnalyzer
from src.physics_constraints import PhysicsConstraints
from src.neural_networks.codonic_network import CodonicNetwork
from src.neural_networks.pinn import PINN
from src.utils.kinematics import forward_kinematics, inverse_kinematics
from src.utils.optimization import optimize_body_model, compute_adaptation_gradient

logger = logging.getLogger(__name__)

class CodonicLayer:
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        pinn_model: PINN,
        body_schema_learner: BodySchemaLearner,
        biomechanical_constraints: BiomechanicalConstraints,
        rynnec_analyzer: RynnECVideoAnalyzer,
        physics_constraints: PhysicsConstraints,
        learning_rate: float = 1e-3,
        device: torch.device = torch.device('cpu')
    ):
        """
        Initialize the CodonicLayer for predictive sensory processing.
        
        Args:
            input_dim: Dimension of input features
            hidden_dim: Hidden layer dimension
            output_dim: Output dimension for sensory predictions
            pinn_model: Physics-Informed Neural Network model
            body_schema_learner: Body schema adaptation system
            biomechanical_constraints: Joint and torque constraints
            rynnec_analyzer: Video analysis system
            physics_constraints: Physical constraint enforcement
            learning_rate: Learning rate for optimization
            device: Computation device
        """
        self.device = device
        self.pinn_model = pinn_model
        self.body_schema_learner = body_schema_learner
        self.biomechanical_constraints = biomechanical_constraints
        self.rynnec_analyzer = rynnec_analyzer
        self.physics_constraints = physics_constraints
        self.sensory_history = []
        self.adaptation_history = []
        
        # Initialize the codonic network
        self.codonic_network = CodonicNetwork(
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            output_dim=output_dim
        ).to(device)
        
        self.optimizer = optim.Adam(
            self.codonic_network.parameters(),
            lr=learning_rate
        )
        
        logger.info("CodonicLayer initialized successfully")

    def predict_sensory_output(
        self,
        joint_angles: torch.Tensor,
        external_forces: Optional[torch.Tensor] = None
    ):
        """
        Predict sensory output based on current body state and external forces.
        
        Args:
            joint_angles: Current joint angles of the body
            external_forces: Optional external forces acting on the body
            
        Returns:
            Predicted sensory output and metadata
        """
        try:
            # Validate inputs
            if not isinstance(joint_angles, torch.Tensor):
                raise TypeError("joint_angles must be a torch.Tensor")
                
            if external_forces is not None and not isinstance(external_forces, torch.Tensor):
                raise TypeError("external_forces must be a torch.Tensor or None")
                
            # Get current body state representation
            body_state = self.body_schema_learner.get_body_state()
            
            # Apply forward kinematics to get current position
            link_lengths = body_state.get('link_lengths', [])
            if link_lengths:
                positions = forward_kinematics(joint_angles, link_lengths)
            else:
                positions = joint_angles  # Fallback if no link lengths available
            
            # Predict sensory state using codonic network
            sensory_prediction = self.codonic_network(positions)
            
            # Apply biomechanical constraints
            constrained_output = self.biomechanical_constraints.apply_joint_limits(sensory_prediction)
            
            # Package metadata
            metadata = {
                'input_positions': positions,
                'raw_output': sensory_prediction,
                'constrained_output': constrained_output,
                'body_state': body_state
            }
            
            logger.debug("Sensory prediction completed successfully")
            return constrained_output, metadata
            
        except Exception as e:
            logger.error(f"Error in predict_sensory_output: {str(e)}")
            raise

    def update_codonic_weights(
        self,
        target_sensory_data: torch.Tensor,
        learning_rate: Optional[float] = None
    ):
        """
        Update the codonic network weights based on target sensory data.
        
        Args:
            target_sensory_data: Ground truth sensory data for training
            learning_rate: Optional learning rate override
            
        Returns:
            Training metrics
        """
        if learning_rate is not None:
            # Temporarily change learning rate if specified
            original_lr = self.optimizer.param_groups[0]['lr']
            self.optimizer.param_groups[0]['lr'] = learning_rate
            
        self.codonic_network.train()
        self.optimizer.zero_grad()
        
        # Get current prediction
        with torch.no_grad():
            current_state = self.body_schema_learner.get_body_state()
            joint_angles = current_state.get('joint_angles', torch.zeros(1))
            prediction, _ = self.predict_sensory_output(joint_angles)
        
        # Compute loss between prediction and target
        loss_fn = nn.MSELoss()
        loss = loss_fn(prediction, target_sensory_data)
        
        # Backpropagate and update weights
        loss.backward()
        self.optimizer.step()
        
        # Reset learning rate if changed
        if learning_rate is not None:
            self.optimizer.param_groups[0]['lr'] = original_lr
            
        self.codonic_network.eval()
        
        # Return training metrics
        metrics = {
            'loss': loss.item(),
            'learning_rate': self.optimizer.param_groups[0]['lr']
        }
        
        logger.info(f"Codonic weights updated. Loss: {loss.item()}")
        return metrics

    def integrate_with_pinn(
        self,
        pinn_model,
        sensory_data: torch.Tensor,
        physics_weight: float = 1.0
    ):
        """
        Integrate codonic layer predictions with PINN model for physics-informed sensory processing.
        
        Args:
            pinn_model: The PINN body model
            sensory_data: Target sensory data to match
            physics_weight: Weight for physics-based loss component
            
        Returns:
            Combined loss value for optimization
        """
        # Get current prediction from codonic layer
        current_state = self.body_schema_learner.get_body_state()
        joint_angles = current_state.get('joint_angles', torch.zeros(1))
        codonic_output, _ = self.predict_sensory_output(joint_angles)
        
        # Compute codonic loss
        codonic_loss = nn.MSELoss()(codonic_output, sensory_data)
        
        # Compute physics-based loss using the PINN model
        physics_loss = pinn_model.compute_physics_loss(codonic_output)
        
        # Combine losses
        total_loss = (1.0 - physics_weight) * codonic_loss + physics_weight * physics_loss
        
        return total_loss