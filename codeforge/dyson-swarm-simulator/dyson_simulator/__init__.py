"""Dyson Swarm Simulator - Package initialization."""

from dyson_simulator.constants import (
    SOLAR_LUMINOSITY,
    DYSON_CAPTURE_EFFICIENCY,
    SOLAR_MASS,
    AU,
    EARTH_MASS,
    LAUNCH_COST_PER_KG,
    MAX_LAUNCH_MASS_RATE,
)

__version__ = "0.1.0"

__all__ = [
    "SOLAR_LUMINOSITY",
    "DYSON_CAPTURE_EFFICIENCY",
    "SOLAR_MASS",
    "AU",
    "EARTH_MASS",
    "LAUNCH_COST_PER_KG",
    "MAX_LAUNCH_MASS_RATE",
]

# Make load_tests available at module level
import unittest


def load_tests(loader, tests, pattern):
    """Function to load tests for the module."""
    return tests

# Export the function so it can be discovered
__all__.append("load_tests")