"""Demo entry point for quantum-sensory-processing."""

import logging
import numpy as np
import torch

from .sensory_processing import QuantumSensoryProcessor
from .magic_state_metrics import calculate_magic_state_metrics, QualiaTracker
from .test_simulations import generate_ambiguous_scenarios, AmbiguityDetector

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def run_demo() -> None:
    """Demonstrate the full quantum-sensory pipeline."""

    processor = QuantumSensoryProcessor(input_dim=10, output_dim=10)
    logger.info("Processor initialized")

    # Normal input
    normal_input = np.random.randn(4, 10).astype(np.float32)
    result = processor.process(normal_input)
    logger.info(f"Normal input → output shape: {result.shape}")

    # Ambiguous input
    ambiguous = generate_ambiguous_scenarios(dim=10, n_samples=3)
    detector = AmbiguityDetector()
    for i in range(ambiguous.size(0)):
        is_amb, entropy, conf = detector.analyze(ambiguous[i])
        logger.info(f"  Sample {i}: ambiguous={is_amb}, entropy={entropy:.3f}, confidence={conf:.3f}")

    output, metrics = processor.process_tensor(ambiguous)
    logger.info(f"Ambiguous input → metrics: {metrics}")
    logger.info(f"Qualia trend: {processor.qualia_trend:.4f}")


if __name__ == "__main__":
    run_demo()
