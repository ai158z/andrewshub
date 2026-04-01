import os
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from src.backend.iit.continuity import maintain_continuity, transfer_awareness
from src.backend.quantum.nodes import NodeManager, QuantumNode
from src.backend.sensors.processing import process_sensor_data, filter_noise

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SimulationResult:
    scenario: str
    timestamp: str
    node_states: List[Dict[str, Any]]
    emergent_behavior: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class BehaviorModel:
    model_id: str
    input_states: List[Dict[str, Any]]
    calculated_behavior: Dict[str, Any]
    timestamp: str

class CustomHTTPException(Exception):
    """Custom HTTP exception to avoid dependency on fastapi"""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class SimulationEngine:
    def __init__(self):
        self.node_manager = NodeManager()
        self.simulation_history: List[Any] = []
        
    def simulate_embodiment(self, scenario: str) -> SimulationResult:
        """Run a full embodiment simulation for the given scenario"""
        try:
            logger.info(f"Starting embodiment simulation for scenario: {scenario}")
            
            # Initialize simulation model
            simulation = type('SimulationModel', (), {
                'id': len(self.simulation_history) + 1,
                'scenario': scenario,
                'timestamp': datetime.utcnow().isoformat(),
                'status': "running",
                'node_states': None,
                'updated_at': None
            })
            
            # Get active nodes for the simulation
            active_nodes = self.node_manager.get_active_nodes()
            
            if not active_nodes:
                logger.warning("No active nodes found for simulation")
                raise CustomHTTPException(status_code=404, detail="No active nodes available for simulation")
            
            # Run simulation across nodes
            node_states = []
            for node in active_nodes:
                # Process sensory input through codonic encoding
                encoded_input = self.encode_sensory_input({
                    "scenario": scenario,
                    "node_id": node.id,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
                # Maintain IIT continuity
                state_vector = self.maintain_continuity({
                    "node_id": node.id,
                    "encoded_input": encoded_input,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
                # Store processed state
                node_states.append({
                    "node_id": node.id,
                    "state_vector": state_vector,
                    "processed_at": datetime.utcnow().isoformat()
                })
                
                # Update simulation object
                simulation.node_states = json.dumps(node_states)
                simulation.updated_at = datetime.utcnow()
            
            # Store simulation result
            self.simulation_history.append(simulation)
            
            # Create and return result
            result = SimulationResult(
                scenario=scenario,
                timestamp=datetime.utcnow().isoformat(),
                node_states=node_states,
                metadata={
                    "nodes_processed": len(node_states),
                    "simulation_id": simulation.id
                }
            )
            
            logger.info(f"Simulation completed successfully for scenario: {scenario}")
            return result
            
        except CustomHTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in embodiment simulation: {str(e)}")
            raise CustomHTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

    def calculate_emergent_behavior(self, input_states: List[Dict[str, Any]]) -> BehaviorModel:
        """Calculate emergent behavior from input states"""
        try:
            # Create model ID based on timestamp
            model_id = f"behavior_model_{datetime.utcnow().isoformat()}"
            
            # Process the input states to detect patterns
            processed_inputs = []
            for state in input_states:
                # Process sensor data if it's raw data
                if 'sensor_data' in state:
                    processed_data = process_sensor_data(state.get('sensor_data', b''))
                    filtered_data = filter_noise(processed_data)
                    processed_inputs.append({
                        "original": state,
                        "processed": filtered_data
                    })
                else:
                    processed_inputs.append(state)
            
            # Calculate emergent behavior using numpy for pattern analysis
            behavior_pattern = self._analyze_behavior_patterns(processed_inputs)
            
            # Create behavior model
            behavior_model = BehaviorModel(
                model_id=model_id,
                input_states=processed_inputs,
                calculated_behavior=behavior_pattern,
                timestamp=datetime.utcnow().isoformat()
            )
            
            logger.info("Emergent behavior calculated successfully")
            return behavior_model
            
        except CustomHTTPException:
            raise
        except Exception as e:
            logger.error(f"Error calculating emergent behavior: {str(e)}")
            raise CustomHTTPException(status_code=500, detail=f"Behavior calculation failed: {str(e)}")

    def _analyze_behavior_patterns(self, processed_inputs: List[Dict]) -> Dict[str, Any]:
        """Analyze input patterns to determine emergent behavior characteristics"""
        try:
            # Convert inputs to numerical representation for analysis
            patterns = []
            for input_state in processed_inputs:
                if isinstance(input_state, dict) and 'processed' in input_state:
                    # Use processed sensor data for analysis
                    data = input_state['processed']
                    if hasattr(data, 'data'):
                        # Extract numerical values for pattern analysis
                        values = list(data.data.values()) if isinstance(data.data, dict) else [data.data]
                        patterns.extend(values)
            
            # Calculate statistical measures of the patterns
            if patterns:
                numpy_patterns = np.array(patterns)
                behavior_characteristics = {
                    "mean_values": np.mean(numpy_patterns, axis=0).tolist() if numpy_patterns.size > 0 else [],
                    "std_deviation": np.std(numpy_patterns, axis=0).tolist() if numpy_patterns.size > 0 else [],
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                return behavior_characteristics
            else:
                return {
                    "mean_values": [], 
                    "std_deviation": [], 
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error analyzing behavior patterns: {str(e)}")
            return {
                "error": f"Analysis failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }

# Instantiate the simulation engine for use
engine = SimulationEngine()