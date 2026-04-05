import logging
import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Tuple, Optional
from src.neural_networks.pinn import PINN
from src.neural_networks.codonic_network import CodonicNetwork
from src.utils.kinematics import forward_kinematics, inverse_kinematics
from src.utils.optimization import optimize_body_model, compute_adaptation_gradient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BodySchemaLearner:
    def __init__(self, 
                 pinn_model: PINN,
                 biomech_constraints: 'BiomechanicalConstraints',
                 video_analyzer: 'RynnECVideoAnalyzer',
                 codonic_layer: CodonicNetwork,
                 physics_constraints: 'PhysicsConstraints',
                 device: torch.device = torch.device('cpu')):
        """
        Initialize the BodySchemaLearner with required components.
        
        Args:
            pinn_model: Pre-initialized PINN body model
            biomech_constraints: Biomechanical constraints handler
            video_analyzer: Video analysis component
            codonic_layer: Codonic processing layer
            physics_constraints: Physics constraints validator
            device: Computation device
        """
        self.pinn_model = pinn_model
        self.biomech_constraints = biomech_constraints
        self.video_analyzer = video_analyzer
        self.codonic_layer = codonic_layer
        self.physics_constraints = physics_constraints
        self.device = device
        
        # Initialize optimizers
        self.pinn_optimizer = torch.optim.Adam(self.pinn_model.parameters(), lr=1e-3) if self.pinn_model else None
        self.codonic_optimizer = torch.optim.Adam(self.codonic_layer.parameters(), lr=1e-3) if self.codonic_layer else None
        
        logger.info("BodySchemaLearner initialized")
        
    def adapt_body_schema(self, 
                        sensory_data: torch.Tensor, 
                        motor_commands: torch.Tensor,
                        adaptation_rate: float = 0.01) -> Dict[str, float]:
        """
        Adapt the body schema based on sensory-motor discrepancies.
        
        Args:
            sensory_data: Current sensory input tensor
            motor_commands: Motor commands sent to actuators
            adaptation_rate: Rate at which to adapt the model
            
        Returns:
            Dictionary of adaptation metrics
        """
        try:
            # Validate inputs
            if not isinstance(sensory_data, torch.Tensor) or not isinstance(motor_commands, torch.Tensor):
                raise TypeError("sensory_data and motor_commands must be torch.Tensor")
                
            # Compute current model prediction
            predicted_sensory = self.pinn_model(motor_commands)
            
            # Compute adaptation gradient
            adaptation_grad = compute_adaptation_gradient(self.pinn_model, sensory_data, predicted_sensory)
            
            # Update model parameters
            with torch.no_grad():
                for param, grad in zip(self.pinn_model.parameters(), adaptation_grad):
                    param -= adaptation_rate * grad
                    param.clamp_(-adaptation_rate, adaptation_rate)
                
            # Update codonic layer
            self.codonic_layer.update_codonic_weights(sensory_data, predicted_sensory)
            
            # Compute metrics
            error = torch.mean((sensory_data - predicted_sensory) ** 2).item()
            
            logger.info(f"Body schema adapted with error: {error}")
            return {
                "adaptation_error": error,
                "model_parameters_updated": True
            }
            
        except Exception as e:
            logger.error(f"Error in adapt_body_schema: {e}")
            raise

    def update_kinematic_model(self, 
                           joint_angles: List[float], 
                           target_positions: List[Tuple[float, float, float]]) -> Dict[str, any]:
        """
        Update the kinematic model based on new observations.
        
        Args:
            joint_angles: Current joint angles
            target_positions: Target end-effector positions
            
        Returns:
            Dictionary with updated kinematic parameters
        """
        try:
            # Convert to tensors
            joint_tensor = torch.tensor(joint_angles, dtype=torch.float32, device=self.device)
            target_tensor = torch.tensor(target_positions, dtype=torch.float32, device=self.device)
            
            # Compute current positions
            current_positions = self.pinn_model(joint_tensor)
            
            # Compute loss and update model
            loss_fn = nn.MSELoss()
            loss = loss_fn(current_positions, target_tensor)
            
            # Optimize
            self.pinn_optimizer.zero_grad()
            loss.backward()
            self.pinn_optimizer.step()
            
            # Apply joint limits
            constrained_joints = self.biomech_constraints.apply_joint_limits(joint_tensor) if self.biomech_constraints else joint_tensor
            
            return {
                "kinematic_loss": loss.item(),
                "updated_joints": constrained_joints.tolist() if hasattr(constrained_joints, 'tolist') else constrained_joints,
                "target_achieved": True
            }
            
        except Exception as e:
            logger.error(f"Error updating kinematic model: {e}")
            raise

    def calibrate_sensorimotor_map(self, 
                                calibration_data: Dict[str, List]) -> Dict[str, any]:
        """
        Calibrate the sensorimotor mapping using provided calibration data.
        
        Args:
            calibration_data: Dictionary containing motor commands and sensory readings
            
        Returns:
            Dictionary with calibration results
        """
        try:
            motor_commands = torch.tensor(calibration_data['motor_commands'], dtype=torch.float32, device=self.device)
            sensory_readings = torch.tensor(calibration_data['sensory_readings'], dtype=torch.float32, device=self.device)
            
            # Get model prediction
            predicted_sensory = self.pinn_model(motor_commands)
            
            # Compute loss
            loss_fn = nn.MSELoss()
            loss = loss_fn(predicted_sensory, sensory_readings)
            
            # Optimize
            self.pinn_optimizer.zero_grad()
            loss.backward()
            self.pinn_optimizer.step()
            
            # Validate with physics constraints
            physics_check = self.physics_constraints.newtonian_mechanics(motor_commands, predicted_sensory) if self.physics_constraints else True
            
            return {
                "calibration_loss": loss.item(),
                "physics_valid": physics_check,
                "calibration_complete": True
            }
            
        except KeyError as e:
            logger.error(f"Missing key in calibration data: {e}")
            raise ValueError(f"Missing required calibration data: {e}")
        except Exception as e:
            logger.error(f"Error in calibrate_sensorimotor_map: {e}")
            raise

    def _validate_model(self, model_output: torch.Tensor, target_output: torch.Tensor) -> bool:
        """Validate model output against physical constraints."""
        try:
            # Check energy conservation
            energy_check = self.physics_constraints.energy_conservation(model_output, target_output) if self.physics_constraints else True
            
            # Check momentum conservation
            momentum_check = self.physics_constraints.momentum_conservation(model_output, target_output) if self.physics_constraints else True
            
            return energy_check and momentum_check
        except Exception as e:
            logger.error(f"Model validation error: {e}")
            return False