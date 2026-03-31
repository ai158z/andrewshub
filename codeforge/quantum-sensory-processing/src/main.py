import logging
from typing import Any, Dict
import numpy as np
import torch
from .sensory_processing import QuantumSensoryProcessor
from .mpnn_model import MPNNModel
from .magic_state_metrics import calculate_magic_state_metrics, QualiaTracker
from .inverse_solver import solve_inverse_problem
from .test_simulations import test_ambiguous_input

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_demo() -> None:
    """
    Entry point for demonstrating the core components of the quantum-sensory-processing library.
    """
    try:
        # Step 1: Initialize Quantum Sensory Processor
        processor: QuantumSensoryProcessor = QuantumSensoryProcessor()
        logger.info("Quantum Sensory Processor initialized.")
        
        # Step 2: Generate synthetic input data (example dimensions)
        input_data: np.ndarray = np.random.rand(5, 10)  # 5 samples, 10 features
        logger.info("Synthetic input data generated.")
        
        # Step 3: Process input data using the quantum sensory processor
        processed_data: np.ndarray = processor.process(input_data)
        logger.info("Input data processed successfully.")
        
        # Step 4: Initialize MPNN Model and perform forward pass
        mpnn_model: MPNNModel = MPNNModel()
        model_input: torch.Tensor = torch.tensor(processed_data, dtype=torch.float32)
        model_output: torch.Tensor = mpnn_model.forward(model_input)
        logger.info("MPNN model forward pass completed.")
        
        # Step 5: Calculate magic state metrics
        metrics: Dict[str, float] = calculate_magic_state_metrics(model_output)
        logger.info(f"Magic State Metrics: {metrics}")
        
        # Step 6: Track qualia using QualiaTracker
        qualia_tracker: QualiaTracker = QualiaTracker()
        qualia_tracker.track(model_output)
        logger.info("Qualia tracking completed.")
        
        # Step 7: Solve inverse problem
        inverse_solution: Any = solve_inverse_problem(model_output)
        logger.info(f"Inverse Problem Solution: {inverse_solution}")
        
        # Step 8: Test ambiguous input handling
        test_result: Any = test_ambiguous_input(input_data)
        logger.info(f"Ambiguous Input Test Result: {test_result}")
        
        logger.info("Demo execution completed successfully.")
        
    except Exception as e:
        logger.error(f"An error occurred during demo execution: {e}", exc_info=True)
        raise  # Re-raise to propagate the exception

if __name__ == "__main__":
    run_demo()