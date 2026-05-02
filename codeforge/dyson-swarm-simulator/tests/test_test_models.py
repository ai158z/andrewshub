import pytest
from dyson_simulator.models import SimulationParameters, SimulationResults

def test_simulation_parameters_initialization():
    test_data = {
        "target_capture_percent": 90.0,
        "launch_mass_rate": 1000.0,
        "solar_luminosity": 3.828e26,
        "dyson_capture_efficiency": 0.5
    }
    
    params = SimulationParameters(
        target_capture_percent=test_data["target_capture_percent"],
        launch_mass_rate=test_data["launch_mass_rate"],
        solar_luminosity=test_data["solar_luminosity"],
        dyson_capture_efficiency=test_data["dyson_capture_efficiency"]
    )
    
    assert params.target_capture_percent == test_data["target_capture_percent"]
    assert params.launch_mass_rate == test_data["launch_mass_rate"]
    assert params.solar_luminosity == test_data["solar_luminosity"]
    assert params.dyson_capture_efficiency == test_data["dyson_capture_efficiency"]

def test_simulation_parameters_to_dict():
    test_data = {
        "target_capture_percent": 90.0,
        "launch_mass_rate": 1000.0,
        "solar_luminosity": 3.828e26,
        "dyson_capture_efficiency": 0.5
    }
    
    params = SimulationParameters(
        target_capture_percent=test_data["target_capture_percent"],
        launch_mass_rate=test_data["launch_mass_rate"],
        solar_luminosity=test_data["solar_luminosity"],
        dyson_capture_efficiency=test_data["dyson_capture_efficiency"]
    )
    
    params_dict = params.to_dict()
    expected_dict = {
        'target_capture_percent': test_data["target_capture_percent"],
        'launch_mass_rate': test_data["launch_mass_rate"],
        'solar_luminosity': test_data["solar_luminosity"],
        'dyson_capture_efficiency': test_data["dyson_capture_efficiency"]
    }
    assert params_dict == expected_dict

def test_simulation_parameters_from_dict():
    params_dict = {
        'target_capture_percent': 90.0,
        'launch_mass_rate': 1000.0,
        'solar_luminosity': 3.828e26,
        'dyson_capture_efficiency': 0.5
    }
    
    params = SimulationParameters.from_dict(params_dict)
    
    assert params.target_capture_percent == 90.0
    assert params.launch_mass_rate == 1000.0
    assert params.solar_luminosity == 3.828e26
    assert params.dyson_capture_efficiency == 0.5

def test_simulation_results_initialization():
    test_result_data = {
        "construction_time": 100,
        "total_mass": 1e9,
        "collector_area": 5e8
    }
    
    results = SimulationResults(
        construction_time=test_result_data["construction_time"],
        total_mass=test_result_data["total_mass"],
        collector_area=test_result_data["collector_area"]
    )
    
    assert results.construction_time == test_result_data["construction_time"]
    assert results.total_mass == test_result_data["total_mass"]
    assert results.collector_area == test_result_data["collector_area"]

def test_simulation_results_to_dict():
    test_result_data = {
        "construction_time": 100,
        "total_mass": 1e9,
        "collector_area": 5e8
    }
    
    results = SimulationResults(
        construction_time=test_result_data["construction_time"],
        total_mass=test_result_data["total_mass"],
        collector_area=test_result_data["collector_area"]
    )
    
    result_dict = results.to_dict()
    expected = {
        'construction_time': test_result_data["construction_time"],
        'total_mass': test_result_data["total_mass"],
        'collector_area': test_result_data["collector_area"]
    }
    assert result_dict == expected

def test_simulation_results_from_dict():
    result_dict = {
        'construction_time': 100,
        'total_mass': 1e9,
        'collector_area': 5e8
    }
    
    results = SimulationResults.from_dict(result_dict)
    
    assert results.construction_time == 100
    assert results.total_mass == 1e9
    assert results.collector_area == 5e8

def test_simulation_parameters_edge_values():
    params = SimulationParameters(
        target_capture_percent=0.0,
        launch_mass_rate=0.0,
        solar_luminosity=0.0,
        dyson_capture_efficiency=0.0
    )
    
    assert params.target_capture_percent == 0.0
    assert params.launch_mass_rate == 0.0
    assert params.solar_luminosity == 0.0
    assert params.dyson_capture_efficiency == 0.0

def test_simulation_parameters_max_values():
    params = SimulationParameters(
        target_capture_percent=100.0,
        launch_mass_rate=1e10,
        solar_luminosity=1e30,
        dyson_capture_efficiency=1.0
    )
    
    assert params.target_capture_percent == 100.0
    assert params.launch_mass_rate == 1e10
    assert params.solar_luminosity == 1e30
    assert params.dyson_capture_efficiency == 1.0

def test_simulation_results_edge_values():
    results = SimulationResults(
        construction_time=0,
        total_mass=0,
        collector_area=0
    )
    
    assert results.construction_time == 0
    assert results.total_mass == 0
    assert results.collector_area == 0

def test_simulation_results_large_values():
    results = SimulationResults(
        construction_time=1000000,
        total_mass=1e15,
        collector_area=1e12
    )
    
    assert results.construction_time == 1000000
    assert results.total_mass == 1e15
    assert results.collector_area == 1e12

def test_simulation_parameters_from_dict_missing_keys():
    params_dict = {
        'target_capture_percent': 90.0
    }
    
    with pytest.raises(KeyError):
        SimulationParameters.from_dict(params_dict)

def test_simulation_results_from_dict_missing_keys():
    result_dict = {
        'construction_time': 100
    }
    
    with pytest.raises(KeyError):
        SimulationResults.from_dict(result_dict)

def test_simulation_parameters_from_dict_extra_keys():
    params_dict = {
        'target_capture_percent': 90.0,
        'launch_mass_rate': 1000.0,
        'solar_luminosity': 3.828e26,
        'dyson_capture_efficiency': 0.5,
        'extra_key': 'extra_value'
    }
    
    params = SimulationParameters.from_dict(params_dict)
    
    assert params.target_capture_percent == 90.0
    assert params.launch_mass_rate == 1000.0
    assert params.solar_luminosity == 3.828e26
    assert params.dyson_capture_efficiency == 0.5

def test_simulation_results_from_dict_extra_keys():
    result_dict = {
        'construction_time': 100,
        'total_mass': 1e9,
        'collector_area': 5e8,
        'extra_key': 'extra_value'
    }
    
    results = SimulationResults.from_dict(result_dict)
    
    assert results.construction_time == 100
    assert results.total_mass == 1e9
    assert results.collector_area == 5e8

def test_simulation_parameters_negative_values():
    params = SimulationParameters(
        target_capture_percent=-10.0,
        launch_mass_rate=-500.0,
        solar_luminosity=-1e25,
        dyson_capture_efficiency=-0.1
    )
    
    assert params.target_capture_percent == -10.0
    assert params.launch_mass_rate == -500.0
    assert params.solar_luminosity == -1e25
    assert params.dyson_capture_efficiency == -0.1

def test_simulation_results_negative_values():
    results = SimulationResults(
        construction_time=-50,
        total_mass=-1e8,
        collector_area=-1e7
    )
    
    assert results.construction_time == -50
    assert results.total_mass == -1e8
    assert results.collector_area == -1e7

def test_simulation_parameters_fractional_values():
    params = SimulationParameters(
        target_capture_percent=99.99,
        launch_mass_rate=0.001,
        solar_luminosity=1.23456789e20,
        dyson_capture_efficiency=0.999
    )
    
    assert params.target_capture_percent == 99.99
    assert params.launch_mass_rate == 0.001
    assert params.solar_luminosity == 1.23456789e20
    assert params.dyson_capture_efficiency == 0.999

def test_simulation_results_fractional_values():
    results = SimulationResults(
        construction_time=0.5,
        total_mass=0.999,
        collector_area=1.001
    )
    
    assert results.construction_time == 0.5
    assert results.total_mass == 0.999
    assert results.collector_area == 1.001