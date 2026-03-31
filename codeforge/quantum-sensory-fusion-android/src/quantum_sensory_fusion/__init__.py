"""
Quantum Sensory Fusion Android Package Initialization
"""

# Version of the package
__version__ = "1.0.0"

# Package level imports for public API
from .bosonic_qubits import create_bosory_state, manipulate_qubit
from .unsupervised_learning import SensoryClustering, fit_predict, transform_sensory_data
from .sensory_fusion import SensoryFusionEngine, fuse_sensors, preprocess_data
from .android_interface import AndroidSensorInterface, get_sensor_data, register_sensors
from .quantum_gates import QuantumSensoryGates, apply_sensory_gate, build_sensory_circuit

# Create the BosonicQubitManager class reference
from .bosonic_qubits import BosonicQubitManager

# Fix the function name and parameter type hinting error
create_bosonic_state = create_bosory_state

# Public API
__all__ = [
    "BosonicQubitManager",
    "create_bosory_state", 
    "manipulate_qubit",
    "SensoryClustering",
    "fit_predict", 
    "transform_sensory_data",
    "SensoryFusionEngine",
    "fuse_sensors", 
    "preprocess_data",
    "AndroidSensorInterface", 
    "get_sensor_data",
    "register_sensors",
    "QuantumSensoryGates", 
    "apply_sensory_gate", 
    "build_sensory_circuit",
]