from typing import Dict, Any
import logging
from src.quantum_sensors.models import SensorFusionData
from src.quantum_sensors.zeno_processor import ZenoProcessor
from src.quantum_sensors.codonic_layer import CodonicProcessor
from src.quantum_sensors.entanglement_handler import EntanglementHandler
from src.quantum_sensors.config import ConfigManager
from src.utils import validate_sensor_data, normalize_quantum_states
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FusionEngine:
    """
    Quantum entanglement-based sensor fusion engine that processes and correlates
    multi-sensory data from visual and tactile sensors.
    """
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.zeno_processor = ZenoProcessor()
        self.codonic_processor = CodonicProcessor()
        self.entanglement_handler = EntanglementHandler()
    
    def fuse_sensors(self, visual_data: Dict[str, Any], tactile_data: Dict[str, Any]) -> SensorFusionData:
        """
        Fuses visual and tactile sensor data using quantum entanglement principles.
        """
        try:
            # Validate input data
            validate_sensor_data(visual_data)
            validate_sensor_data(tactile_data)
            
            # Normalize quantum states
            normalized_visual = normalize_quantum_states(visual_data)
            normalized_tactile = normalize_quantum_states(tactile_data)
            
            # Apply codonic processing
            processed_visual = self.codonic_processor.process_codonic_layer(normalized_visual)
            processed_tactile = self.codonic_processor.process_codonic_layer(normalized_tactile)
            
            # Apply quantum entanglement correlation
            entangled_output = self.entanglement_handler.correlate_sensors(
                processed_visual, 
                processed_tactile
            )
            
            # Apply Zeno stabilization for perceptual continuity
            stabilized_data = self.zeno_processor.apply_zeno_stabilization(entangled_output)
            
            # Extract timestamp from the stabilized data
            if isinstance(stabilized_data, dict):
                timestamp = stabilized_data.get('timestamp', '')
            else:
                # If not a dict, try to get timestamp from one of the input data sources
                timestamp = visual_data.get('timestamp', tactile_data.get('timestamp', ''))
            
            # Create fused data model
            fused_data = SensorFusionData(
                timestamp=timestamp,
                sensor_data=stabilized_data,
                fusion_metadata={
                    "processing_steps": [
                        "data_validation",
                        "quantum_normalization", 
                        "codonic_processing",
                        "entanglement_correlation",
                        "zeno_stabilization"
                    ]
                }
            )
            
            logger.info("Sensor fusion completed successfully")
            return fused_data
            
        except Exception as e:
            logger.error(f"Sensor fusion failed: {str(e)}")
            raise RuntimeError(f"Failed to fuse sensors: {str(e)}") from e

# Module-level function for direct access
fusion_engine = FusionEngine()

def fuse_sensors(visual_data: Dict[str, Any], tactile_data: Dict[str, Any]) -> SensorFusionData:
    """
    Module-level function to fuse sensor data using quantum entanglement principles.
    """
    return fusion_engine.fuse_sensors(visual_data, tactile_data)