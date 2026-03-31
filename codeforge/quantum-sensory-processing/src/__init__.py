"""Quantum-inspired sensory processing library for android embodiment."""

from .sensory_processing import QuantumSensoryProcessor
from .mpnn_model import MPNNModel
from .magic_state_metrics import calculate_magic_state_metrics, QualiaTracker
from .inverse_solver import solve_inverse_problem
from .test_simulations import AmbiguityDetector, check_ambiguous_input

__all__ = [
    "QuantumSensoryProcessor",
    "MPNNModel",
    "calculate_magic_state_metrics",
    "QualiaTracker",
    "solve_inverse_problem",
    "AmbiguityDetector",
    "check_ambiguous_input",
]
