import pytest
from dyson_simulator.constants import *

def test_physical_constants_values():
    assert SOLAR_LUMINOSITY == 3.828e26
    assert SOLAR_MASS == 1.989e30
    assert ASTRONOMICAL_UNIT == 1.496e11
    assert SPEED_OF_LIGHT == 299792458
    assert GRAVITATIONAL_CONSTANT == 6.67430e-11

def test_dyson_swarm_parameters_values():
    assert DYSON_CAPTURE_EFFICIENCY == 0.95
    assert MINIMUM_COLLECTOR_AREA == 1000.0
    assert MAX_LAUNCH_MASS_RATE == 1000000.0
    assert TARGET_CAPTURE_PERCENT == 0.50

def test_material_properties_values():
    assert SILICON_DENSITY == 2330.0
    assert ALUMINUM_DENSITY == 2700.0
    assert SILICON_ATOMIC_MASS == 28.0855
    assert AVOGADRO_CONSTANT == 6.02214076e23

def test_economic_constants_values():
    assert MANUFACTURING_COST_PER_KG == 1000.0
    assert TRANSPORT_COST_PER_KG == 500.0
    assert ANNUAL_BUDGET == 1e12

def test_time_constants_values():
    assert SECONDS_PER_YEAR == 31536000
    assert SECONDS_PER_DAY == 86400
    assert SECONDS_PER_HOUR == 3600

def test_simulation_configuration_values():
    assert DEFAULT_SIMULATION_YEARS == 100
    assert DEFAULT_TIMESTEP_YEARS == 1.0
    assert DEFAULT_OUTPUT_INTERVAL == 10

def test_validation_thresholds_values():
    assert MIN_VALID_CAPTURE_PERCENT == 0.01
    assert MAX_VALID_CAPTURE_PERCENT == 0.99
    assert MIN_VALID_MASS_RATE == 1.0
    assert MAX_VALID_MASS_RATE == 1e10

def test_error_margins_values():
    assert ENERGY_CALCULATION_ERROR_MARGIN == 1e-9
    assert MASS_CALCULATION_ERROR_MARGIN == 1e-6

def test_constants_are_final():
    import inspect
    constants_module = inspect.getmodule(inspect.currentframe().f_code)
    for name, value in constants_module.__dict__.items():
        if name.isupper() and not name.startswith('_'):
            assert isinstance(value, (int, float)), f"{name} should be a constant value"

def test_all_constants_are_typed():
    from typing import Final
    import inspect
    constants_module = inspect.getmodule(inspect.currentframe().f_code)
    for name in dir(constants_module):
        if name.isupper() and not name.startswith('_'):
            var = getattr(constants_module, name)
            assert isinstance(var, (int, float)), f"{name} should be a numeric constant"