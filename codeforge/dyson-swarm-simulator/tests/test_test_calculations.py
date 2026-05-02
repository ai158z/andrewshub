import pytest
import numpy as np
from dyson_simulator.calculations import (
    calculate_timeline,
    calculate_mass_requirements,
    calculate_collector_area
)
from dyson_simulator.constants import (
    SOLAR_LUMINOSITY,
    DYSON_CAPTURE_EFFICIENCY,
    SOLAR_MASS,
    STELLAR_LIFETIME
)

def test_calculate_timeline_normal():
    result = calculate_timeline(50.0, 1000.0)
    assert isinstance(result, float)
    assert result > 0

def test_calculate_timeline_zero_rate():
    result = calculate_timeline(50.0, 0.0)
    assert result == float('inf')

def test_calculate_timeline_zero_capture():
    result = calculate_timeline(0.0, 1000.0)
    assert result == 0.0

def test_calculate_timeline_high_capture():
    result = calculate_timeline(95.0, 1000.0)
    assert isinstance(result, float)

def test_calculate_mass_requirements_normal():
    result = calculate_mass_requirements(50.0)
    assert isinstance(result, float)
    assert result >= 0

def test_calculate_mass_requirements_zero():
    result = calculate_mass_requirements(0.0)
    assert result == 0.0

def test_calculate_mass_requirements_full():
    result = calculate_mass_requirements(100.0)
    assert isinstance(result, float)

def test_calculate_collector_area_normal():
    result = calculate_collector_area(50.0)
    assert isinstance(result, float)
    assert result >= 0

def test_calculate_collector_area_zero():
    result = calculate_collector_area(0.0)
    assert result == 0.0

def test_calculate_collector_area_full():
    result = calculate_collector_area(100.0)
    assert isinstance(result, float)

def test_collector_area_increases_with_capture():
    area_low = calculate_collector_area(25.0)
    area_high = calculate_collector_area(75.0)
    assert area_high >= area_low

def test_calculate_timeline_negative_capture():
    with pytest.raises((ValueError, ZeroDivisionError)):
        calculate_timeline(-10.0, 1000.0)

def test_calculate_timeline_negative_rate():
    result = calculate_timeline(50.0, -1000.0)
    assert result == float('inf')

def test_calculate_mass_requirements_negative():
    with pytest.raises(ValueError):
        calculate_mass_requirements(-10.0)

def test_calculate_collector_area_negative():
    with pytest.raises(ValueError):
        calculate_collector_area(-10.0)

def test_calculate_timeline_boundary_values():
    result = calculate_timeline(100.0, 1000.0)
    assert isinstance(result, float)

def test_calculate_mass_requirements_boundary():
    result = calculate_mass_requirements(100.0)
    assert isinstance(result, float)

def test_calculate_collector_area_boundary():
    result = calculate_collector_area(100.0)
    assert isinstance(result, float)

def test_timeline_inf_case():
    result = calculate_timeline(50.0, 0.0)
    assert np.isinf(result)

def test_timeline_zero_case():
    result = calculate_timeline(0.0, 1000.0)
    assert result == 0.0