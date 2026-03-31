import json
import logging
from typing import Any, Dict, Optional
import numpy as np

class StatePersistence:
    def __init__(self, storage_path: str = "quantonic_states.json"):
        self.storage_path = storage_path
        self.logger = logging.getLogger(__name__)

    def save_state(self, state_data: Dict[str, Any], filepath: Optional[str] = None) -> bool:
        try:
            save_path = filepath or self.storage_path
            serialized_data = self.serialize_quantum_state(state_data)
            
            with open(save_path, 'w') as f:
                f.write(serialized_data)
                
            self.logger.info(f"State saved successfully to {save_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save state: {str(e)}")
            return False

    def serialize_quantum_state(self, state_data: Dict[str, Any]) -> str:
        try:
            serializable_data = {}
            for key, value in state_data.items():
                if isinstance(value, np.ndarray):
                    serializable_data[key] = value.tolist()
                elif isinstance(value, dict):
                    # Handle nested quantum states
                    nested_data = {}
                    for k, v in value.items():
                        if isinstance(v, np.ndarray):
                            nested_data[k] = v.tolist()
                        else:
                            nested_data[k] = v
                    serializable_data[key] = nested_data
                else:
                    serializable_data[key] = value
            return json.dumps(serializable_data)
        except Exception as e:
            self.logger.error(f"Serialization failed: {str(e)}")
            raise

    def deserialize_quantum_state(self, data: str) -> Dict[str, Any]:
        try:
            parsed = json.loads(data)
            result = {}
            for key, value in parsed.items():
                if isinstance(value, dict):
                    result[key] = {k: np.array(v) if isinstance(v, list) else v for k, v in value.items()}
                elif isinstance(value, list):
                    result[key] = np.array(value)
                else:
                    result[key] = value
            return result
        except Exception as e:
            self.logger.error(f"Deserialization failed: {str(e)}")
            raise

    def load_state(self, filepath: Optional[str] = None) -> Optional[Dict[str, Any]]:
        try:
            load_path = filepath or self.storage_path
            with open(load_path, 'r') as f:
                data = f.read()
            return self.deserialize_quantum_state(data)
        except FileNotFoundError:
            self.logger.warning(f"State file not found: {load_path}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to load state: {str(e)}")
            return None

    def backup_state(self, state, backup_path: str) -> bool:
        try:
            state_data = state.get_state()
            serialized = self.serialize_quantum_state({'state': state_data})
            with open(backup_path, 'w') as f:
                f.write(serialized)
            self.logger.info(f"State backup saved to {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to backup state: {str(e)}")
            return False