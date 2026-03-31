import torch
import numpy as np
import logging
from typing import Tuple, Dict, Optional

from .mpnn_model import MPNNModel
from .magic_state_metrics import calculate_magic_state_metrics, QualiaTracker
from .inverse_solver import solve_inverse_problem
from .test_simulations import check_ambiguous_input

logger = logging.getLogger(__name__)


class QuantumSensoryProcessor:
    """Quantum-inspired sensory processing pipeline.

    Pipeline:
        1. Encode raw sensor data through the MPNN
        2. Compute magic-state metrics (qualia indicators)
        3. Detect ambiguity — if ambiguous, run inverse calibration
        4. Track qualia trend over time
    """

    def __init__(
        self,
        input_dim: int = 10,
        output_dim: int = 10,
        hidden_dim: int = 32,
        ambiguity_threshold: float = 0.85,
    ):
        self.model = MPNNModel(
            input_dim=input_dim, output_dim=output_dim, hidden_dim=hidden_dim
        )
        self.qualia_tracker = QualiaTracker()
        self.ambiguity_threshold = ambiguity_threshold

    def process(self, raw_input: np.ndarray) -> np.ndarray:
        """Process raw numpy sensor data and return processed output as numpy."""
        tensor = torch.tensor(raw_input, dtype=torch.float32)
        output, _ = self.process_tensor(tensor)
        return output.detach().numpy()

    def process_tensor(
        self, input_data: torch.Tensor
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        """Full pipeline on a torch tensor.

        Returns:
            (output_tensor, magic_state_metrics)
        """
        output = self.model(input_data)
        metrics = calculate_magic_state_metrics(output)
        self.qualia_tracker.update(metrics)

        if check_ambiguous_input(input_data, entropy_threshold=self.ambiguity_threshold):
            logger.info("Ambiguous input detected — running inverse calibration")
            inv = solve_inverse_problem(output, model=self.model, max_steps=100)
            calibrated = inv["optimized_input"]
            output = self.model(calibrated)
            metrics = calculate_magic_state_metrics(output)
            self.qualia_tracker.update(metrics)

        return output, metrics

    @property
    def qualia_trend(self) -> float:
        return self.qualia_tracker.trend()
