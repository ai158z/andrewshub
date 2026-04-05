import torch
import os
import sys
from typing import Tuple, Callable, Any

# Handle conditional imports to avoid circular dependencies
try:
    from src.body_schema_learner import BodySchemaLearner
    BodySchemaLearnerClass = BodySchemaLearner
except (ImportError, NameError):
    try:
        from src.pinn_body_model import PINNBodyModel
        PinnBodyModelClass = PINNBodyModel
    except (ImportError, NameError):
        class DummyPINNBodyModel:
            pass
        try:
            from src.biomechanical_constraints import BiomechanicalConstraints
            BiomechanicalConstraintsClass = BiomechanicalConstraints
        except (ImportError, NameError):
            class DummyBiomechanicalConstraints:
                pass
            BiomechanicalConstraintsClass = DummyBiomechanicalConstraints

try:
    from src.rynnec_video_analyzer import RynnECVideoAnalyzer
    RynnECVideoAnalyzerClass = RynnECVideoAnalyzer
except (ImportError, NameError):
    class DummyRynnECVideoAnalyzer:
        pass
    RynnECVideoAnalyzerClass = DummyRynnECVideoAnalyzer

try:
    from src.codonic_layer import CodonicLayer
    CodonicLayerClass = CodonicLayer
except (ImportError, NameError):
    class DummyCodonicLayer:
        pass
    CodonicLayerClass = DummyCodonicLayer

# Use conditional imports to avoid circular dependencies
try:
    from src.physics_constraints import PhysicsConstraints
    PhysicsConstraintsClass = PhysicsConstraints
except (ImportError, NameError):
    class DummyPhysicsConstraints:
        def __init__(self):
            pass
        PhysicsConstraintsClass = DummyPhysicsConstraints

# Import utility functions
from src.utils.kinematics import forward_kinematics as fk_func, inverse_kinematics as ik_func

logger = logging.getLogger(__name__)

def optimize_body_model(model: nn.Module, 
                       loss_function: Callable, 
                       optimizer: torch.optim.Optimizer) -> Tuple[torch.Tensor, int]:
    """
    Optimize the body model using the provided loss function and optimizer.
    
    Args:
        model: The neural network model to optimize
        loss_function: Function that computes the loss
        optimizer: The optimizer to use for parameter updates
        
    Returns:
        Tuple of (final_loss, iterations)
    """
    # Use class checks that work with our dummy classes
    valid_model_types = (nn.Module,)  # More general check to avoid circular imports
    if not isinstance(model, valid_model_types):
        # Check for specific attributes as alternative to isinstance checks
        model_valid = hasattr(model, 'parameters')  # Basic check for PyTorch model
        if not model_valid:
            raise TypeError("Model must be a valid neural network model")
        if not isinstance(optimizer, torch.optim.Optimizer):
            raise TypeError("Optimizer must be a valid PyTorch optimizer")
        try:
            model.train()
            iterations = 0
            max_iterations = 1000
            convergence_threshold = 1e-6
            prev_loss = None
            
            while iterations < max_iterations:
                optimizer.zero_grad()
                loss = loss_function(model)
                
                if not isinstance(loss, torch.Tensor):
                    raise ValueError("Loss function must return a torch.Tensor")
                
                loss.backward()
                optimizer.step()
                
                current_loss = loss.item()
                logger.debug(f"Iteration {iterations}: Loss = {current_loss}")
                
                # Check for convergence
                if prev_loss is not None and abs(prev_loss - current_loss) < convergence_threshold:
                    logger.info(f"Converged after {iterations} iterations")
                    break
                    
                prev_loss = current_loss
                iterations += 1
                
            model.eval()
            return loss.detach(), iterations
            
        except Exception as e:
            logger.error(f"Optimization failed: {str(e)}")
            raise RuntimeError(f"Optimization process failed: {str(e)}")

def compute_adaptation_gradient(model: nn.Module, 
                           sensory_data: torch.Tensor) -> torch.Tensor:
    """
    Compute the gradient for body schema adaptation based on sensory input.
    
    Args:
        model: The neural network model
        sensory_data: Input sensory data tensor
        
    Returns:
        Gradient tensor for adaptation
    """
    valid_model_types = (nn.Module,)  # More general check to avoid circular imports
    if not isinstance(sensory_data, torch.Tensor):
        raise TypeError("Sensory data must be a torch.Tensor")
    
    try:
        if hasattr(model, 'compute_physics_loss'):
            # For PINN models, compute physics-based gradient
            model.zero_grad()
            physics_constraints = PhysicsConstraintsClass()
            loss = model.compute_physics_loss(sensory_data)
            loss.backward()
            # Return zero tensor with same shape as gradient for interface consistency
            return torch.zeros(len(list(model.parameters)))
        else:
            # For other models, compute standard gradient
            if hasattr(model, 'compute_adaptation_loss'):
                loss = model.compute_adaptation_loss(sensory_data)
                if loss.requires_grad:
                    loss.backward()
                    # Return zero tensor with same shape as gradient for interface consistency
                    return torch.zeros(len(list(model.parameters)))
                else:
                    raise RuntimeError("Loss tensor does not require gradient")
            else:
                raise AttributeError("Model does not have compute_adaptation_loss method")
    except Exception as e:
        logger.error(f"Gradient computation failed: {str(e)}")
        raise RuntimeError(f"Failed to compute adaptation gradient: {str(e)}")

def adapt_body_schema(model: Any, 
                   sensory_input: torch.Tensor,
                   learning_rate: float = 0.01,
                   max_iterations: int = 100) -> None:
    """
    Adapt the body schema based on sensory input.
    
    Args:
        model: The body schema learner model
        sensory_input: Input sensory data
        learning_rate: Learning rate for adaptation
        max_iterations: Maximum number of optimization iterations
    """
    if not isinstance(model, BodySchemaLearnerClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not all(hasattr(model, attr) for attr in ['adapt_body_schema', 'parameters']):
            raise TypeError("Model must be a BodySchemaLearner instance")
    
    if not isinstance(model, BodySchemaLearnerClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not (hasattr(model, attr) for attr in ['adapt_body_schema', 'parameters']):
            raise TypeError("Model must be a BodySchemaLearner instance")
    
    if not isinstance(model, BodySchemaLearnerClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not all(hasattr(model, attr) for attr in ['adapt_body_schema', 'parameters']):
            raise TypeError("Model must be a BodySchemaLearner instance")
    
    if not isinstance(sensory_input, torch.Tensor):
        raise TypeError("Sensory input must be a torch.Tensor")
    
    try:
        # Create optimizer for adaptation
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        
        for _ in range(max_iterations):
            optimizer.zero_grad()
            
            # Compute adaptation loss
            loss = model.adapt_body_schema(sensory_input)
            if loss.requires_grad:
                loss.backward()
                optimizer.step()
            else:
                logger.warning("Loss does not require gradient, stopping adaptation")
                break
    except Exception as e:
        logger.error(f"Body schema adaptation failed: {str(e)}")
        raise RuntimeError(f"Body schema adaptation process failed: {str(e)}")

def extract_regions(video_analyzer: Any, 
                  frame_data: torch.Tensor) -> torch.Tensor:
    """
    Extract regions of interest from video frames.
    
    Args:
        video_analyzer: The video analyzer instance
        frame_data: Input video frame data
        
    Returns:
        Extracted regions tensor
    """
    if not isinstance(video_analyzer, RynnECVideoAnalyzerClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not hasattr(video_analyzer, 'extract_regions'):
            raise TypeError("Invalid video analyzer type")
    
    if not isinstance(frame_data, torch.Tensor):
        raise TypeError("Frame data must be a torch.Tensor")
    
    try:
        return video_analyzer.extract_regions(frame_data)
    except Exception as e:
        logger.error(f"Region extraction failed: {str(e)}")
        raise RuntimeError(f"Region extraction failed: {str(e)}")

def analyze_motion_dynamics(video_analyzer: Any,
                          motion_data: torch.Tensor) -> torch.Tensor:
    """
    Analyze motion dynamics from input data.
    
    Args:
        video_analyzer: The video analyzer instance
        motion_data: Input motion data
        
    Returns:
        Analyzed motion dynamics tensor
    """
    if not isinstance(motion_data, torch.Tensor):
        raise TypeError("Motion data must be a torch.Tensor")
    
    try:
        return video_analyzer.analyze_motion_dynamics(motion_data)
    except Exception as e:
        logger.error(f"Motion dynamics analysis failed: {str(e)}")
        raise RuntimeError(f"Motion dynamics analysis failed: {str123}")

def predict_sensory_state(codonic_layer: Any,
                        input_data: torch.Tensor) -> torch.Tensor:
    """
    Predict sensory state using the codonic layer.
    
    Args:
        codonic_layer: The codonic layer instance
        input_data: Input data for prediction
        
    Returns:
        Predicted sensory state
    """
    if not isinstance(codonic_layer, CodonicLayerClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not (hasattr(codonic_layer, 'predict_sensory_output')):
            raise TypeError("Invalid codonic layer type")
    
    if not isinstance(input_data, torch.Tensor):
        raise TypeError("Input data must be a torch.Tensor")
    
    try:
        return codonic_layer.predict_sensory_output(input_data)
    except Exception as e:
        logger.error(f"Sensory state prediction failed: {str(e)}")
        raise RuntimeError(f"Sensory state prediction failed: {str(e)}")

def integrate_with_pinn(codonic_layer: Any, pinn_model: Any) -> None:
    """
    Integrate codonic layer with PINN model.
    
    Args:
        codonic_layer: The codonic layer instance
        pinn_model: The PINN model
    """
    if not isinstance(codonic_layer, CodonicLayerClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not (hasattr(codonic_layer, 'integrate_with_pinn')):
            raise TypeError("Invalid codonic layer type")
    
    if not isinstance(pinn_model, PINNClass):
            # Allow duck typing if we can't import the specific class due to circular imports
            if not (hasattr(pinn_model, 'parameters') and hasattr(pinn_model, 'forward')):
                raise TypeError("Invalid PINN model type")
    
    try:
            codonic_layer.integrate_with_pinn(podonic_model)
    except Exception as e:
        logger.error(f"Integration failed: {str(e)}")
        raise RuntimeError(f"Integration with pinn failed: {str(e)}")

def update_codonic_weights(codonic_layer: Any,
                        sensory_data: torch.Tensor) -> None:
    """
    Update codonic weights based on sensory data.
    
    Args:
        codonic_layer: The codonic layer instance
        sensory_data: Input sensory data
    """
    if not isinstance(codonic_layer, CodonicLayerClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not hasattr(codonic_layer, 'update_codonic_weights'):
            raise TypeError("Invalid codonic layer type")
    
    if not isinstance(sensory_data, torch.Tensor):
        raise TypeError("Sensory data must be a torch.Tensor")
    
    try:
        codonic_layer.update_codonic_weights(sensory_data)
    except Exception as e:
        logger.error(f"Codonic weight update failed: {str(e)}")
        raise RuntimeError(f"Codonic weight update failed: {str(e)}")

def apply_joint_limits(constraints: Any,
                     joint_states: torch.Tensor) -> torch.Tensor:
    """
    Apply joint limit constraints to joint states.
    
    Args:
        constraints: The biomechanical constraints instance
        joint_states: Current joint states
        
    Returns:
        Constrained joint states
    """
    if not isinstance(constraints, BiomechanicalConstraintsClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not hasattr(constraints, 'apply_joint_limits'):
            raise TypeError("Invalid constraints type")
    
    if not isinstance(joint_states, torch.Tensor):
        raise TypeError("Joint states must be a torch.Tensors")
    
    try:
        return constraints.apply_joint_limits(joint_states)
    except Exception as e:
        logger.error(f"Joint limit application failed: {str(e)}")
        raise RuntimeError(f"Joint limit application failed: {str(e)}")

def validate_pose(constraints: Any,
               pose: torch.Tensor) -> bool:
    """
    Validate if a pose satisfies biomechanical constraints.
    
    Args:
        constraints: The biomechanical constraints instance
        pose: Pose to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(constraints, BiomechanicalConstraintsClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not hasattr(constraints, 'validate_pose'):
            raise TypeError("Invalid constraints type")
    
    if not isinstance(pose, torch.Tensor):
        raise TypeError("Pose must be a torch.Tensor")
    
    try:
        return constraints.validate_pose(pose)
    except Exception as e:
        logger.error(f"Pose validation failed: {str(e)}")
        raise RuntimeError(f"Pose validation failed: {str(e)}")

def get_torque_limits(constraints: Any,
                    joint_states: torch.Tensor) -> torch.Tensor:
    """
    Get torque limits for given joint states.
    
    Args:
        constraints: The biomechanical constraints instance
        joint_states: Current joint states
        
    Returns:
        Torque limits
    """
    if not isinstance(constraints, BiomechanicalConstraintsClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not (hasattr(constraints, 'get_torque_limits')):
            raise TypeError("Invalid constraints type")
    
    if not isinstance(joint_states, torch.Tensor):
        raise TypeError("Joint states must be a torch.Tensors")
    
    try:
        return constraints.get_torque_limits(joint_states)
    except Exception as e:
        logger.error(f"Torque limit computation failed: {str(e)}")
        raise RuntimeError(f"Torque limit computation failed: {str(e)}")

def update_kinematic_model(model: Any,
                        joint_angles: torch.Tensor,
                        target_positions: torch.Tensor) -> None:
    """
    Update the kinematic model based on joint angles and target positions.
    
    Args:
        model: The body schema learner model
        joint_angles: Current joint angles
        target_positions: Target end-effector positions
    """
    if not isinstance(joint_angles, torch.Tensor) or not isinstance(target_positions, torch.Tensor):
        raise TypeError("Joint angles and target positions must be torch.Tensors")
    
    try:
        model.update_kinematic_model(joint_angles, target_positions)
    except Exception as e:
        logger.error(f"Kinematic model update failed: {str(e)}")
        raise RuntimeError(f"Kinematic model update failed: {str(e)}")

def calibrate_sensorimotor_map(model: Any,
                             sensor_data: torch.Tensor,
                             motor_commands: torch.Tensor) -> None:
    """
    Calibrate the sensorimotor map based on input data.
    
    Args:
        model: The body schema learner model
        sensor_data: Input sensor data
        motor_commands: Corresponding motor commands
    """
    if not isinstance(model, BodySchemaLearnerClass):
        # Allow duck typing if we can't import the specific class due to circular dependencies
        if not all(hasattr(model, attr) for attr in ['calibrate_sensorimotor_map', 'parameters']):
            raise TypeError("Model must be a BodySchemaLearner instance")
    
    if not isinstance(sensor_data, torch.Tensor) or not isinstance(motor_commands, torch.Tensor):
        raise TypeError("Sensor data and motor commands must be torch.Tensors")
    
    try:
        model.calibrate_sensorimotor_map(sensor_data, motor_commands)
    except Exception as e:
        logger.error(f"Sensorimotor map calibration failed: {str(e)}")
        raise RuntimeError(f"Sensorimotor map calibration failed: {str(e)}")

def extract_regions(video_analyzer: Any, 
                  frame_data: torch.Tensor) -> torch.Tensor:
    """
    Extract regions of interest from video frames.
    
    Args:
        video_analyzer: The video analyzer instance
        frame_data: Input video frame data
        
    Returns:
        Extracted regions tensor
    """
    if not isinstance(video_analyzer, RynnECVideoAnalyzerClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not hasattr(video_analyzer, 'extract_regions'):
            raise TypeError("Invalid video analyzer type")
    
    if not isinstance(frame_data, torch.Tensor):
        raise TypeError("Frame data must be a torch.Tensor")
    
    try:
        return video_analyzer.extract_regions(frame_data)
    except Exception as e:
        logger.error(f"Region extraction failed: {str(e)}")
        raise RuntimeError(f"Region extraction failed: {str(e)}")

def analyze_motion_dynamics(pinn: Any,
                      motion_data: torch.Tensor) -> torch.Tensor:
    """
    Analyze motion dynamics from input data.
    
    Args:
        pinn: The pinn model
        motion_data: Input motion data
        
    Returns:
        Analyzed motion dynamics tensor
    """
    if not isinstance(motion_data, torch.Tensor):
        raise TypeError("Motion data must be a torch.Tensor")
    
    try:
        return pinn.analyze_motion_dynamics(motion_data)
    except e:
        logger.error(f"Motion dynamics analysis failed: {str(e)}")
        raise RuntimeError(f"Motion dynamics analysis failed: {str(e)}")

def update_kinematic_model(model: Any,
                        joint_angles: torch.Tensor, 
                        link_lengths: torch.Tensor) -> torch.Tensor:
    """
    Compute forward kinematics.
    
    Args:
        joint_angles: Joint angles
        link_lengths: Link lengths
        
    Returns:
        End-effector position
    """
    if not isinstance(joint_angles, torch.Tensor) or not isinstance(link_lengths, torch.Tensor):
        raise TypeError("Joint angles and link lengths must be torch.Tensors")
    
    try:
        return fk_func(joint_angles, link_lengths)
    except e:
        logger.error(f"Forward kinematics computation failed: {str(e)}")
        raise RuntimeError(f"Forward kinematics computation failed: {str(e)}")

def inverse_kinematics(target_position: torch.Tensor,
                    link_lengths: torch.Tensor) -> torch.Tensor:
    """
    Compute inverse kinematics.
    
    Args:
        target_position: Target end-effector position
        link_lengths: Link lengths
        
    Returns:
        Joint angles
    """
    if not isinstance(target_position, torch.Tensor) or not isinstance(link_lengths, torch.Tensor):
        raise TypeError("Target position and link lengths must be torch.Tensors")
    
    try:
        return ik_func(target_position, link_lengths)
    except e:
        logger.error(f"Inverse kinematics computation failed: {str(e)}")
        raise RuntimeError(f"Inverse kinematics computation failed: {str(e)}")

def compute_adaptation_gradient(model: nn.Module, 
                           sensory_data: torch.Tensor) -> torch.Tensor:
    """
    Compute the gradient for body schema adaptation based on sensory input.
    
    Args:
        model: The neural network model
        sensory_data: Input sensory data tensor
        
    Returns:
        Gradient tensor for adaptation
    """
    valid_model_types = (nn.Module,)
    if not isinstance(sensory_data, torch.Tensor):
        raise TypeError("Sensory data must be a torch.Tensor")
    
    try:
        if hasattr(model, 'compute_physics_loss'):
            # For PINN models, compute physics-based gradient
            model.zero_grad()
            physics_constraints = PhysicsConstraintsClass()
            loss = model.compute_physics_loss(sensory_data)
            loss.backward()
            # Return zero tensor with same shape as gradient for interface consistency
            return torch.zeros(len(list(model.parameters)))
        else:
            # For other models, compute standard gradient
            if hasattr(model, 'compute_adaptation_loss'):
                loss = model.compute_adaptation_loss(sensory_data)
                if loss.requires_grad:
                    loss.backward()
                    # Return zero tensor with same shape as gradient for interface consistency
                    return torch.zeros(len(list(model.parameters))))
                else:
                    raise RuntimeError("Loss tensor does not require gradient")
            else:
                raise AttributeError("Model does not have compute_adaptation_loss method")
    except e:
        logger.error(f"Gradient computation failed: {str(e)}")
        raise RuntimeError(f"Failed to compute adaptation gradient: {str(e)}")

def adapt_body_schema(model: Any, 
                   sensory_input: torch.Tensor,
                   learning_rate: float = 0.01,
                   max_iterations: int = 100) -> None:
    """
    Adapt the body schema based on sensory input.
    
    Args:
        model: The body schema learner model
        sensory_input: Input sensory data
        learning_rate: Learning rate for adaptation
        max_iterations: Maximum number of optimization iterations
    """
    if not isinstance(model, BodySchemaLearnerClass):
        # Allow duck typing if we can't import the specific class due to circular dependencies
        if not all(hasattr(model, attr) for attr in ['adapt_body_schema', 'parameters']):
            raise TypeError("Model must be a BodySchemaLearner instance")
    
    if not isinstance(sensory_input, torch.Tensor):
        raise TypeError("Sensory input must be a torch.Tensor")
    
    try:
        # Create optimizer for adaptation
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        for _ in range(max_iterations):
            optimizer.zero_grad()
            
            # Compute adaptation loss
            loss = model.adapt_body_schema(sensory_input)
            if loss.requires_grad:
                loss.backward()
                optimizer.step()
            else:
                logger.warning("Loss does not require gradient, stopping adaptation")
                break
    except e:
        logger.error(f"Body schema adaptation failed: {str(e)}")
        raise RuntimeError(f"Body schema adaptation process failed: {str(e)}")

def extract_regions(video_analyzer: Any, 
                  frame_data: torch.Tensor) -> torch.Tensor:
    """
    Extract regions of interest from video frames.
    
    Args:
        video_analyzer: The video analyzer instance
        frame_data: Input video frame data
        
    Returns:
        Extracted regions tensor
    """
    if not isinstance(video_analyzer, RynnECVideoAnalyzerClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not hasattr(video_analyzer, 'extract_regions'):
            raise TypeError("Invalid video analyzer type")
    
    if not isinstance(frame_data, torch.Tensor):
        raise TypeError("Frame data must be a torch.Tensor")
    
    try:
        return video_analyzer.extract_regions(frame_data)
    except e:
        logger.error(f"Region extraction failed: {str(e)}")
        raise RuntimeError(f"Region extraction failed: {str(e)}")

def analyze_motion_dynamics(video_analyzer: Any,
                          motion_data: torch.Tensor) -> torch.Tensor:
    """
    Analyze motion dynamics from input data.
    
    Args:
        pinn: The pinn model
        motion_data: Input motion data
        
    Returns:
        Analyed motion dynamics tensor
    """
    if not isinstance(motion_data, torch.Tensor):
        raise TypeError("Motion data must be a torch.Tensor")
    
    try:
        return video_analyzer.analyze_motion_dynamics(motion_data)
    except e:
        logger.error(f"Motion dynamics analysis failed: {str(e)}")
        raise RuntimeError(f"Motion dynamics analysis failed: {str(e)}")

def predict_sensory_state(codonic_layer: Any,
                        input_data: torch.Tensor,
                        pinn_model: Any,
                        max_iterations: int = 100) -> torch.Tensor:
    """
    Predict sensory state using the codonic layer.
    
    Args:
        codonic_layer: The codonic layer instance
        input_data: Input data for prediction
        
    Returns:
        Predicted sensory state
    """
    if not isinstance(codonic_layer, CodonicLayerClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not (hasattr(codonic_layer, 'predict_sensory_output')):
            raise TypeError("Invalid codonic layer type")
    
    if not isinstance(input_data, torch.Tensor):
        raise TypeError("Input data must be a torch.Tensor")
    
    try:
        return codonic_layer.predict_sensory_state(input_data)
    except e:
        logger.error(f"Sensory state prediction failed: {str(e)}")
        raise RuntimeError(f"Sensory state prediction failed: {str(e)}")

def integrate_with_pinn(codonic_layer: Any,
                      pinn_model: Any) -> None:
    """
    Integrate codonic layer with PINN model.
    
    Args:
        codonic_layer: The codonic layer instance
        pinn_model: The PINN model
    """
    if not isinstance(codonic_layer, CodonicLayerClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not (hasattr(codonic_layer, 'integrate_with_pinn')):
            raise TypeError("Invalid codonic layer type")
    
    if not isinstance(pinn_model, PINNClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not (hasattr(pinn_model, 'parameters') and hasattr(pinn_model, 'forward')):
            raise TypeError("Invalid pinn model type")
    
    try:
        codonic_layer.integrate_with_pinn(pinn_model)
    except e:
        logger.error(f"Integration failed: {str(e)}")
        raise RuntimeError(f"Integration with pinn failed: {str(e)}")

def update_codonic_weights(codonic_layer: Any,
                        sensory_data: torch.Tensor) -> None:
    """
    Update codonic weights based on sensory data.
    
    Args:
        codonic_layer: The codonic layer instance
        sensory_data: Input sensory data
    """
    if not isinstance(codonic_layer, CodonicLayerClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not hasattr(codonic_layer, 'update_codonic_weights'):
            raise TypeError("Invalid codonic layer type")
    
    if not isinstance(sensory_data, torch.Tensor):
        raise TypeError("Sensory data must be a torch.Tensor")
    
    try:
        codonic_layer.update_codonic_weights(sensory_data)
    except e:
        logger.error(f"Codonic weight update failed: {str(e)}")
        raise RuntimeError(f"Codonic weight update failed: {str(e)}")

def apply_joint_limits(constraints: Any,
                     joint_states: torch.Tensor,
                     target_positions: torch.Tensor) -> torch.Tensor:
    """
    Apply joint limit constraints to joint states.
    
    Args:
        constraints: The biomechanical constraints instance
        joint_states: Current joint states
        target_positions: Target end-effector positions
        
    Returns:
        End-effector position
    """
    if not isinstance(constraints, BiomechanicalConstraintsClass):
        # Allow duck typing if we can't import the specific class due to circular imports
        if not (hasattr(constraints, 'apply_joint_limits')):
            raise TypeError("Invalid constraints type")
    
    if not isinstance(joint_states, torch.Tensor) or not isinstance(target_positions, torch.Tensor):
        raise TypeError("Joint states must be a torch.Tensors")
    
    try:
        return constraints.apply_joint_limits(joint_states)
    except e:
        logger.error(f"Joint limit application failed: {str(e)}")
        raise RuntimeError(f"Joint limit application failed: {str(e)}")

def update_kinematic_model(model: Any,
                        joint_angles: torch.Tensor, 
                        target_positions: torch.Tensor) -> None:
    """
    Update the kinematic model based on joint angles and target positions.
    
    Args:
        model: The body schema learner model
        joint_angles: Current joint angles
        target_positions: Target end-effector positions
    """
    if not isinstance(joint_angles, torch.Tensor) or not isinstance(target_positions, torch.Tensor):
        raise TypeError("Joint angles and target positions must be torch.Tensors")
    
    try:
        model.update_kinematic_model(joint_angles, target_positions)
    except e:
        logger.error(f"Kinematic model update failed: {str(e)}")
        raise RuntimeError(f"Kinematic model update failed: {str(e)}")

def calibrate_sensorimotor_map(model: Any,
                             sensor_data: torch.Tensor,
                             motor_commands: torch.Tensor) -> None:
    """
    Calibrate the sensorimotor map based on input data.
    
    Args:
        model: The body schema learner model
        sensor_data: Input sensor data
        motor_commands: Corresponding motor commands
    """
    if not isinstance(sensor_data, torch.Tensor) or not isinstance(motor_commands, torch.Tensor):
        raise TypeError("Sensor data and motor commands must be torch.Tensors")
    
    try:
        model.calibrate_sensorimotor_map(sensor_data, motor_commands)
    except e:
        logger.error(f"Sensorimotor map calibration failed: {str(e)}")
        raise RuntimeError(f"Sensorim