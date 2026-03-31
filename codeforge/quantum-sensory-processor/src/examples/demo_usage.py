import logging
from typing import Dict, List
import sys
import os

# Add the src directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the required modules
from src.quantum_sensory_processor import QuantumSensoryProcessor
from src.magic_state_distillation import MagicStateDistillation
from src.sensory_integration import SensoryIntegration
from src.quantum_inverse_solver import QuantumInverseSolver
from src.embodied_context import EmbodiedContext
from src.utils import tensor_product

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting quantum sensory processor demo")

def main():
    try:
        # Initialize components
        processor = QuantumSensoryProcessor()
        distiller = MagicStateDistillation()
        integrator = SensoryIntegration()
        solver = QuantumInverseSolver()
        context = EmbodiedContext()
        
        # Process sensory data
        raw_data = {"visual": [0.5, 0.3, 0.2], "auditory": [0.1, 0.9]}
        processed_data = processor.process_sensory_data(raw_data)
        logger.info(f"Processed data: {processed_data}")
        
        # Resolve ambiguity
        resolved_data = processor.resolve_ambiguity(processed_data)
        logger.info(f"Resolved data: {resolved_data}")
        
        # Distill states
        states = ["state1", "state2", "state3"]
        distilled_states = distiller.distill(states)
        logger.info(f"Distilled states: {distilled_states}")
        
        # Purify states
        purified_states = distiller.purify_states(distilled_states)
        logger.info(f"Purified states: {purified_states}")
        
        # Calculate fidelity
        fidelity = distiller.calculate_fidelity(distilled_states)
        logger.info(f"State fidelity: {fidelity}")
        
        # Integrate sensory data
        integrated_data = integrator.integrate_sensory_data([processed_data, resolved_data])
        logger.info(f"Integrated data: {integrated_data}")
        
        # Resolve conflicts
        conflicts = [{"data": "conflict1"}, {"data": "conflict2"}]
        resolved_conflicts = integrator.resolve_conflicts(conflicts)
        logger.info(f"Resolved conflicts: {resolved_conflicts}")
        
        # Solve inverse problem
        solution = solver.solve_inverse_problem(integrated_data)
        logger.info(f"Solution: {solution}")
        
        # Validate solution
        is_valid = solver.validate_solution(solution)
        logger.info(f"Solution valid: {is_valid}")
        
        # Apply context
        contextualized_data = context.apply_context(solution)
        logger.info(f"Contextualized data: {contextualized_data}")
        
        # Tensor product
        state_vector = [0.7, 0.3]
        result = tensor_product(state_vector)
        logger.info(f"Tensor product result: {result}")
        
        # Get final state
        final_state = processor.get_state()
        logger.info(f"Final state: {final_state}")
        
        logger.info("Demo usage script executed successfully")
        print("Demo execution completed")
        
    except Exception as e:
        logger.error(f"Error in demo: {e}")
        print(f"Demo execution failed with error: {e}")

if __name__ == "__main__":
    main()