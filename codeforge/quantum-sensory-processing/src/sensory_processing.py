import logging
import torch
from torch import Tensor
from typing import Tuple, Dict
from .mpnn_model import MPNNModel
from .magic_state_metrics import calculate_magic_state_metrics, QualiaTracker
from .inverse_solver import solve_inverse_problem
from .test_simulations import test_ambiguous_input

class QuantumSensoryProcessor:
    def __init__(self):
        self.model = MPNNModel()
        self.qualia_tracker = QualiaTracker()
        self.logger = logging.getLogger(__name__)

    def process_data(self, input_data: Tensor) -> Tuple[Tensor, Dict[str, float]]:
        """Process sensory data using the quantum-inspired pipeline.

        Args:
            input_data: Input tensor representing sensory data.

        Returns:
            A tuple containing the processed output tensor and a dictionary of magic state metrics.

        Raises:
            ValueError: If input data is not a PyTorch Tensor.
            RuntimeError: If any step of processing fails.
        """
        if not isinstance(input_data, Tensor):
            raise ValueError("Input data must be a PyTorch Tensor")
        
        try:
            # Forward pass through the MPNN model
            output = self.model.forward(input_data)
        except Exception as e:
            self.logger.error("MPNN model forward pass failed", exc_info=True)
            raise RuntimeError("Model processing failed") from e

        # Calculate magic state metrics from the output
        try:
            metrics = calculate_magic_state_metrics(output)
        except Exception as e:
            self.logger.error("Magic state metrics calculation failed", exc_info=True)
            raise RuntimeError("Metrics calculation failed") from e

        # Update qualia tracker with the computed metrics
        self.qualia_tracker.update(metrics)

        # Check for ambiguous input using test simulation
        try:
            is_ambiguous = test_ambiguous_input(input_data)
        except Exception as e:
            self.logger.warning("Ambiguous input check failed", exc_info=True)
            is_ambiguous = False  # Default to non-ambiguous if check fails

        if is_ambiguous:
            try:
                # Solve the inverse problem for ambiguous inputs
                inverse_solution = solve_inverse_problem(input_data)
                self.logger.info("Applied inverse solution for ambiguous input")
                # Modify output based on inverse solution (example logic)
                output = inverse_solution * output
                # Recalculate metrics after modifying output
                try:
                    metrics = calculate_magic_state_metrics(output)
                except Exception as e:
                    self.logger.error("Magic state metrics recalculation failed", exc_info=True)
                    raise RuntimeError("Metrics recalculation failed") from e
                # Update qualia tracker with the new metrics
                self.qualia_tracker.update(metrics)
            except Exception as e:
                self.logger.error("Inverse problem solving failed", exc_info=True)
                raise RuntimeError("Inverse solution failed") from e

        return output, metrics