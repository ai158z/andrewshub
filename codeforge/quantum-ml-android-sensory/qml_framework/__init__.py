import sys
from typing import Any, Dict, List
import logging

# Setup logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

class QMLFramework:
    """Main framework class that integrates all QML components"""
    
    def __init__(self):
        self.core = None
        self.sensory = None
        self.q_layers = None
        self.bridge = None
        self.framework = {
            'status': 'initialized',
            'data': {},
            'version': '1.0.0'
        }
        
    def __getattr__(self, name: str) -> Any:
        # Import modules locally to avoid circular imports
        from qml_framework import core, sensory_input, quantum_layers, android_bridge
        
        if name == 'sensory':
            if self.sensory is None:
                self.sensory = sensory_input.SensoryInputProcessor()
            return self.sensory
        elif name == 'core':
            if self.core is None:
                self.core = core.CoreProcessor()
            return self.core
        elif name == 'q_layers':
            if self.q_layers is None:
                self.q_layers = quantum_layers.QuantumLayerProcessor()
            return self.q_layers
        elif name == 'bridge':
            if self.bridge is None:
                self.bridge = android_bridge.AndroidBridge()
            return self.bridge
        else:
            raise AttributeError(f"'QMLFramework' object has no attribute '{name}'")
    
    def __dir__(self) -> List[str]:
        # Return the list of available attributes
        return ['core', 'sensory', 'q_layers', 'bridge']

# Create a framework instance
framework = QMLFramework()

# Initialize the framework components
def initialize_components():
    """Initialize framework components in a lazy manner"""
    # Components will be initialized on first access
    pass

# Main framework instance
QMLFramework()