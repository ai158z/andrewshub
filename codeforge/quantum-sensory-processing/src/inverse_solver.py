import torch
import numpy as np
import logging
from typing import Dict, Any, Optional

from .mpnn_model import MPNNModel

logger = logging.getLogger(__name__)


def solve_inverse_problem(
    target_output: torch.Tensor,
    model: Optional[MPNNModel] = None,
    lr: float = 0.01,
    max_steps: int = 500,
    tolerance: float = 1e-6,
) -> Dict[str, Any]:
    """Find an input that produces the desired output from the MPNN.

    Uses gradient-based optimization (no scipy dependency, no eval).

    Args:
        target_output: The desired output tensor.
        model: An MPNNModel instance.  If None a default is created.
        lr: Learning rate for the optimizer.
        max_steps: Maximum optimization steps.
        tolerance: Early-stop when loss drops below this.

    Returns:
        Dict with optimized_input, final loss, convergence flag, and step count.
    """
    if model is None:
        out_dim = target_output.shape[-1] if target_output.dim() > 0 else 1
        model = MPNNModel(input_dim=out_dim, output_dim=out_dim)
    model.eval()

    # Initialize learnable input
    input_tensor = torch.randn_like(target_output, requires_grad=True)
    optimizer = torch.optim.Adam([input_tensor], lr=lr)
    loss_history = []

    for step in range(max_steps):
        optimizer.zero_grad()
        prediction = model(input_tensor)
        loss = torch.nn.functional.mse_loss(prediction, target_output.detach())
        loss.backward()
        optimizer.step()

        loss_val = loss.item()
        loss_history.append(loss_val)

        if loss_val < tolerance:
            logger.info(f"Inverse solver converged at step {step} (loss={loss_val:.2e})")
            break

    return {
        "optimized_input": input_tensor.detach(),
        "loss": loss_history[-1],
        "converged": loss_history[-1] < tolerance,
        "steps": len(loss_history),
    }
