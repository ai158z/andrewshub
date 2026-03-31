import os
import logging
from typing import Dict, Any
from src.sensory.quantum_processor import QuantumProcessor
from src.sensory.orch_or_engine import OrchOREngine
from src.perception.adaptation import PerceptionAdaptation
from src.perception.pattern_recognition import PatternRecognition
from src.feedback.actuator import ActuatorController
from src.feedback.response_generator import ResponseGenerator
from src.models.sensory_data import SensoryData
from src.utils.signal_processing import process_signal
from src.utils.quantum_math import quantum_fourier_transform


# Configure logging
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


class SensoryInputHandler:
    def __init__(self):
        self.quantum_processor = QuantumProcessor()
        self.orch_or_engine = OrchOREngine()
        self.perception_adaptation = PerceptionAdaptation()
        self.pattern_recognition = PatternRecognition()
        self.actuator_controller = ActuatorController()
        self.response_generator = ResponseGenerator()

    def process_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming sensory data through the full pipeline:
        1. Validate and parse input data
        2. Process quantum state
        3. Apply ORCH-OR engine
        4. Adapt perception
        5. Recognize patterns
        6. Generate feedback
        7. Control actuators
        """
        try:
            # Validate input data
            sensory_data = SensoryData(**data)
            
            # Process signal
            processed_signal = process_signal(sensory_data.signal)
            logger.info("Signal processed successfully")
            
            # Apply quantum fourier transform
            qft_result = quantum_fourier_transform(processed_signal)
            logger.info("Quantum Fourier Transform applied")
            
            # Process quantum state
            quantum_data = self.quantum_processor.process_quantum_state({
                "signal": qft_result,
                "metadata": sensory_data.metadata
            })
            logger.info("Quantum state processed")
            
            # Compute ORCH-OR state
            orch_or_data = self.orch_or_engine.compute_orch_or_state(quantum_data)
            logger.info("ORCH-OR state computed")
            
            # Adapt perception
            adapted_data = self.perception_adaptation.adapt_to_input({
                "quantum_state": orch_or_data,
                "sensory_input": data
            })
            logger.info("Perception adapted to input")
            
            # Recognize patterns
            patterns = self.pattern_recognition.recognize_patterns(adapted_data.get("patterns", []))
            logger.info("Patterns recognized")
            
            # Generate feedback
            feedback = self.response_generator.generate_feedback({
                "patterns": patterns,
                "perception_data": adapted_data
            })
            logger.info("Feedback generated")
            
            # Control actuators
            actuator_response = self.actuator_controller.control_response(feedback)
            logger.info("Actuator response controlled")
            
            return {
                "status": "success",
                "input_data": data,
                "processed_signal": processed_signal,
                "quantum_data": quantum_data,
                "orch_or_data": orch_or_data,
                "adapted_perception": adapted_data,
                "patterns": patterns,
                "feedback": feedback,
                "actuator_response": actuator_response
            }
            
        except Exception as e:
            logger.error(f"Error processing input: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "input_data": data
            }