import torch
import numpy as np
from scipy.optimize import minimize
from src.mpnn_model import MPNNModel
from src.sensory_processing import QuantumSensoryProcessor
from src.magic_state_metrics import QualiaTracker, calculate_magic_state_metrics
import logging
from typing import Optional, Dict, Any
import os

logger = logging.getLogger(__name__)

def solve_inverse_problem(
    target_output: torch.Tensor,
    initial_guess: Optional[torch.Tensor] = None,
    optimization_options: Dict[str, Any] = {}
) -> Dict[str, Any]:
    """
    Solves the inverse problem to find the input that produces the given target output from the MPNN model.
    
    Args:
        target_output (torch.Tensor): The desired output tensor from the MPNN model.
        initial_guess (torch.Tensor, optional): Initial guess for the input. Defaults to random if not provided.
        optimization_options (Dict[str, Any], optional): Options for the optimization process. Defaults to {}.
    
    Returns:
        Dict[str, Any]: Dictionary containing the optimized input, loss history, and other relevant metrics.
    
    Raises:
        TypeError: If target_output or initial_guess are of incorrect type.
        EnvironmentError: If MPNN_MODEL_PATH environment variable is not set.
        RuntimeError: If model loading or optimization fails.
    """
    
    # Input validation
    if not isinstance(target_output, torch.Tensor):
        raise TypeError("target_output must be a torch.Tensor")
    if initial_guess is not None and not isinstance(initial_guess, torch.Tensor):
        raise TypeError("initial_guess must be a torch.Tensor or None")
    
    # Load MPNN model from environment variable path
    model_path = os.environ.get('MPNN_MODEL_PATH')
    if model_path is None:
        raise EnvironmentError("MPNN_MODEL_PATH environment variable not set")
    
    try:
        # Load the model
        model = MPNNModel.load_from_checkpoint(model_path)
        model.eval()
    except Exception as e:
        logger.error(f"Failed to load MPNN model: {e}")
        raise RuntimeError("Unable to load MPNN model") from e
    
    # Initialize sensory processor and qualia tracker
    sensory_processor = QuantumSensoryProcessor()
    qualia_tracker = QualiaTracker()
    
    # Prepare initial guess if not provided
    if initial_guess is None:
        # Infer input dimension from model parameters (example: first linear layer)
        input_dim = next(model.parameters()).shape[1] if hasattr(model, 'input_dim') else 10
        initial_guess = torch.randn(input_dim)
    
    # Define the objective function to minimize
    def objective(params: np.ndarray) -> float:
        # Convert numpy array to torch tensor
        input_tensor = torch.tensor(params, dtype=torch.float32)
        with torch.no_grad():
            prediction = model.forward(input_tensor)
            loss = torch.nn.functional.mse_loss(prediction, target_output)
        qualia_tracker.track(loss.item())  # Track loss in qualia tracker
        return loss.item()
    
    # Convert initial guess to numpy array for scipy optimizer
    initial_guess_np = initial_guess.numpy()
    
    # Optimization using scipy's minimize
    try:
        result = minimize(objective, initial_guess_np, method='L-BFGS-B', options=optimization_options)
    except Exception as e:
        logger.error(f"Optimization failed: {e}")
        raise RuntimeError("Inverse problem optimization failed") from e
    
    # Check if optimization was successful
    if not result.success:
        logger.warning(f"Optimization did not converge: {result.message}")
    
    # Convert optimized parameters back to torch tensor
    optimized_input = torch.tensor(result.x, dtype=torch.float32)
    
    # Calculate magic state metrics for the optimized input
    magic_metrics = calculate_magic_state_metrics(optimized_input)
    
    # Log results
    logger.info(f"Optimization completed. Final loss: {result.fun}")
    logger.info(f"Optimized input: {optimized_input}")
    
    # Return results
    return {
        'optimized_input': optimized_input,
        'loss': result.fun,
        'magic_state_metrics': magic_metrics,
        'success': result.success,
        'message': result.message
    }