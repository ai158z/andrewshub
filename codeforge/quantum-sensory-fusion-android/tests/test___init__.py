import pytest
from unittest.mock import patch, Mock

def test_bosonic_qubit_manager_import():
    """Test that BosonicQubitManager can be imported from package"""
    from src.quantum_sensory_fusion import BosonicQubitManager
    assert BosonicQubitManager is not None

def test_create_bosory_state_import():
    """Test that create_bosonic_state can be imported from package"""
    from src.quantum_sensory_fusion import create_bosory_state
    assert create_bosory_state is not None

def test_manipulate_qubit_import():
    """Test that manipulate_qubit can be imported from package"""
    from src.quantum_sensory_fusion import manipulate_qubit
    assert manipulate_qubit is not None

def test_sensory_clustering_import():
    """Test that SensoryClustering can be imported from package"""
    from src.quantum_sensory_fusion import SensoryClustering
    assert SensoryClustering is not None

def test_fit_predict_import():
    """Test that fit_predict can be imported from package"""
    from src.quantum_sensory_fusion import fit_predict
    assert fit_predict is not None

def test_transform_sensory_data_import():
    """Test that transform_sensory_data can be imported from package"""
    from src.quantum_sensory_fusion import transform_sensory_data
    assert transform_sensory_data is not None

def test_sensory_fusion_engine_import():
    """Test that SensoryFusionEngine can be imported from package"""
    from src.quantum_sensory_fusion import SensoryFusionEngine
    assert SensoryFusionEngine is not None

def test_fuse_sensors_import():
    """Test that fuse_sensors can be imported from package"""
    from src.quantum_sensory_fusion import fuse_sensors
    assert fuse_sensors is not None

def test_preprocess_data_import():
    """Test that preprocess_data can be imported from package"""
    from src.quantum_sensory_fusion import preprocess_data
    assert preprocess_data is not None

def test_android_sensor_interface_import():
    """Test that AndroidSensorInterface can be imported from package"""
    from src.quantum_sensory_fusion import AndroidSensorInterface
    assert AndroidSensorInterface is not None

def test_get_sensor_data_import():
    """Test that get_sensor_data can be imported from package"""
    from src.quantum_sensory_fusion import get_sensor_data
    assert get_sensor_data is not None

def test_register_sensors_import():
    """Test that register_sensors can be imported from package"""
    from src.quantum_sensory_fusion import register_sensors
    assert register_sensors is not None

def test_quantum_sensory_gates_import():
    """Test that QuantumSensoryGates can be imported from package"""
    from src.quantum_sensory_fusion import QuantumSensoryGates
    assert QuantumSensoryGates is not None

def test_apply_sensory_gate_import():
    """Test that apply_sensory_gate can be imported from package"""
    from src.quantum_sensory_fusion import apply_sensory_gate
    assert apply_sensory_gate is not None

def test_build_sensory_circuit_import():
    """Test that build_sensory_circuit can be imported from package"""
    from src.quantum_sensory_fusion import build_sensory_circuit
    assert build_sensory_circuit is not None

def test_version_defined():
    """Test that __version__ is properly defined"""
    import src.quantum_sensory_fusion
    assert src.quantum_sensory_fusion.__version__ == "1.0.0"

def test_all_list_complete():
    """Test that __all__ list contains expected public API elements"""
    import src.quantum_sensory_fusion
    expected_exports = [
        "BosonicQubitManager", "create_bosonic_state", "manipulate_qubit",
        "SensoryClustering", "fit_predict", "transform_sensory_data",
        "SensoryFusionEngine", "fuse_sensors", "preprocess_data",
        "AndroidSensorInterface", "get_sensor_data", "register_sensors",
        "QuantumSensoryGates", "apply_sensory_gate", "build_sensory_circuit"
    ]
    
    for export in expected_exports:
        assert export in src.quantum_sensory_fusion.__all__

def test_package_imports_work():
    """Test that all package imports work correctly"""
    from src.quantum_sensory_fusion import (
        BosonicQubitManager, create_bosory_state, manipulate_qubit,
        SensoryClustering, fit_predict, transform_sensory_data,
        SensoryFusionEngine, fuse_sensors, preprocess_data,
        AndroidSensorInterface, get_sensor_data, register_sensors,
        QuantumSensoryGates, apply_sensory_gate, build_sensory_circuit
    )

def test_duplicate_exports_warning():
    """Test that there are no duplicate entries in __all__"""
    import src.quantum_sensory_fusion
    all_list = src.quantum_sensory_fusion.__all__
    assert len(all_list) == len(set(all_list)), "Duplicate entries found in __all__"

def test_required_public_apis_present():
    """Test that all required public APIs are exported"""
    import src.quantum_sensory_fusion
    required_apis = [
        'BosonicQubitManager', 'SensoryClustering', 'SensoryFusionEngine',
        'AndroidSensorInterface', 'QuantumSensoryGates'
    ]
    
    all_apis = src.quantum_sensory_fusion.__all__
    for api in required_apis:
        assert api in all_apis, f"Required API {api} not in __all__"