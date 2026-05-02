import pytest
from dyson_simulator.calculations import calculate_timeline, calculate_mass_requirements, calculate_collector_area
from dyson_simulator.models import SimulationResults
from dyson_simulator.constants import SOLAR_LUMINOSITY, DYSON_CAPTURE_EFFICIENCY, SOLAR_MASS, COLLECTOR_EFFICIENCY

def test_calculate_timeline_valid_inputs():
    result = calculate_timeline(50.0, 100.0)
    assert isinstance(result, SimulationResults)
    assert result.timeline_in_years > 0
    assert result.target_capture_percentage == 50.0

def test_calculate_timeline_zero_capture_percent():
    with pytest.raises(ValueError, match="Target capture percentage must be between 0 and 100"):
        calculate_timeline(0, 100)

def test_calculate_timeline_negative_capture_percent():
    with pytest.raises(ValueError, match="Target capture percentage must be between 0 and 100"):
        calculate_timeline(-10, 100)

def test_calculate_timeline_over_100_capture_percent():
    with pytest.raises(ValueError, match="Target capture percentage must be between 0 and 100"):
        calculate_timeline(101, 100)

def test_calculate_timeline_zero_launch_mass_rate():
    with pytest.raises(ValueError, match="Launch mass rate must be positive"):
        calculate_timeline(50, 0)

def test_calculate_timeline_negative_launch_mass_rate():
    with pytest.raises(ValueError, match="Launch mass rate must be positive"):
        calculate_timeline(50, -10)

def test_calculate_mass_requirements_valid_inputs():
    result = calculate_mass_requirements(75.0)
    assert isinstance(result, SimulationResults)
    assert result.required_mass > 0
    assert result.collector_area > 0

def test_calculate_mass_requirements_zero_capture_percent():
    with pytest.raises(ValueError, match="Target capture percentage must be between 0 and 100"):
        calculate_mass_requirements(0)

def test_calculate_mass_requirements_negative_capture_percent():
    with pytest.raises(ValueError, match="Target capture percentage must be between 0 and 100"):
        calculate_mass_requirements(-20)

def test_calculate_mass_requirements_over_100_capture_percent():
    with pytest.raises(ValueError, match="Target capture percentage must be between 0 and 100"):
        calculate_mass_requirements(120)

def test_calculate_collector_area_valid_inputs():
    area = calculate_collector_area(60.0)
    expected_area = SOLAR_LUMINOSITY * 0.6 * COLLECTOR_EFFICIENCY
    assert area == expected_area

def test_calculate_collector_area_zero_capture_percent():
    with pytest.raises(ValueError, match="Target capture percentage must be between 0 and 100"):
        calculate_collector_area(0)

def test_calculate_collector_area_negative_capture_percent():
    with pytest.raises(ValueError, match="Target capture percentage must be between 0 and 100"):
        calculate_collector_area(-30)

def test_calculate_collector_area_over_100_capture_percent():
    with pytest.raises(ValueError, match="Target capture percentage must be between 0 and 100"):
        calculate_collector_area(110)

def test_calculate_timeline_high_capture_low_launch_rate():
    result1 = calculate_timeline(90, 10)
    result2 = calculate_timeline(90, 100)
    assert result1.timeline_in_years > result2.timeline_in_years

def test_calculate_timeline_low_capture_high_launch_rate():
    result1 = calculate_timeline(10, 1000)
    result2 = calculate_timeline(10, 100)
    assert result1.timeline_in_years < result2.timeline_in_years

def test_calculate_mass_requirements_proportional_to_capture():
    result1 = calculate_mass_requirements(25)
    result2 = calculate_mass_requirements(75)
    assert result2.required_mass > result1.required_mass

def test_calculate_collector_area_proportional_to_capture():
    area1 = calculate_collector_area(25)
    area2 = calculate_collector_area(75)
    assert area2 > area1

def test_mass_requirements_consistent_with_constants():
    capture_percent = 50.0
    result = calculate_mass_requirements(capture_percent)
    expected_mass = SOLAR_MASS * (capture_percent / 100)
    expected_area = expected_mass * DYSON_CAPTURE_EFFICIENCY * COLLECTOR_EFFICIENCY
    assert result.required_mass == expected_mass
    assert result.collector_area == expected_area

def test_collector_area_consistent_with_constants():
    capture_percent = 40.0
    area = calculate_collector_area(capture_percent)
    expected_area = SOLAR_LUMINOSITY * (capture_percent / 100) * COLLECTOR_EFFICIENCY
    assert area == expected_area