import pytest
from dyson_simulator.models import SimulationParameters, SimulationResults

def test_simulation_parameters_valid():
    params = SimulationParameters(
        target_capture_percent=85.0,
        launch_mass_rate=1000.0,
        simulation_duration=365,
        num_swarms=10,
        swarm_size=100,
        replication_factor=1.5,
        maintenance_factor=0.8,
        energy_efficiency=90.0,
        resource_efficiency=85.0
    )
    assert params.target_capture_percent == 85.0
    assert params.launch_mass_rate == 1000.0

def test_simulation_parameters_invalid_capture_percent_negative():
    with pytest.raises(ValueError, match="Target capture percentage must be between 0 and 100"):
        SimulationParameters(
            target_capture_percent=-5.0,
            launch_mass_rate=1000.0,
            simulation_duration=365,
            num_swarms=10,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0
        )

def test_simulation_parameters_invalid_capture_percent_over_100():
    with pytest.raises(ValueError, match="Target capture percentage must be between 0 and 100"):
        SimulationParameters(
            target_capture_percent=105.0,
            launch_mass_rate=1000.0,
            simulation_duration=365,
            num_swarms=10,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0
        )

def test_simulation_parameters_invalid_launch_mass_rate():
    with pytest.raises(ValueError, match="Launch mass rate must be positive"):
        SimulationParameters(
            target_capture_percent=85.0,
            launch_mass_rate=0,
            simulation_duration=365,
            num_swarms=10,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0
        )

def test_simulation_parameters_invalid_simulation_duration():
    with pytest.raises(ValueError, match="Simulation duration must be positive"):
        SimulationParameters(
            target_capture_percent=85.0,
            launch_mass_rate=1000.0,
            simulation_duration=0,
            num_swarms=10,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0
        )

def test_simulation_parameters_invalid_num_swarms():
    with pytest.raises(ValueError, match="Number of swarms must be positive"):
        SimulationParameters(
            target_capture_percent=85.0,
            launch_mass_rate=1000.0,
            simulation_duration=365,
            num_swarms=0,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0
        )

def test_simulation_parameters_invalid_swarm_size():
    with pytest.raises(ValueError, match="Swarm size must be positive"):
        SimulationParameters(
            target_capture_percent=85.0,
            launch_mass_rate=1000.0,
            simulation_duration=365,
            num_swarms=10,
            swarm_size=-5,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0
        )

def test_simulation_parameters_invalid_replication_factor():
    with pytest.raises(ValueError, match="Replication factor must be positive"):
        SimulationParameters(
            target_capture_percent=85.0,
            launch_mass_rate=1000.0,
            simulation_duration=365,
            num_swarms=10,
            swarm_size=100,
            replication_factor=0,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0
        )

def test_simulation_parameters_invalid_maintenance_factor():
    with pytest.raises(ValueError, match="Maintenance factor must be positive"):
        SimulationParameters(
            target_capture_percent=85.0,
            launch_mass_rate=1000.0,
            simulation_duration=365,
            num_swarms=10,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=-0.5,
            energy_efficiency=90.0,
            resource_efficiency=85.0
        )

def test_simulation_parameters_invalid_energy_efficiency():
    with pytest.raises(ValueError, match="Energy efficiency must be between 0 and 100"):
        SimulationParameters(
            target_capture_percent=85.0,
            launch_mass_rate=1000.0,
            simulation_duration=365,
            num_swarms=10,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=105.0,
            resource_efficiency=85.0
        )

def test_simulation_parameters_invalid_resource_efficiency():
    with pytest.raises(ValueError, match="Resource efficiency must be between 0 and 100"):
        SimulationParameters(
            target_capture_percent=85.0,
            launch_mass_rate=1000.0,
            simulation_duration=365,
            num_swarms=10,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=-5.0
        )

def test_simulation_parameters_to_dict():
    params = SimulationParameters(
        target_capture_percent=85.0,
        launch_mass_rate=1000.0,
        simulation_duration=365,
        num_swarms=10,
        swarm_size=100,
        replication_factor=1.5,
        maintenance_factor=0.8,
        energy_efficiency=90.0,
        resource_efficiency=85.0
    )
    result = params.to_dict()
    assert isinstance(result, dict)
    assert result["target_capture_percent"] == 85.0
    assert result["launch_mass_rate"] == 1000.0

def test_simulation_results_valid():
    results = SimulationResults(
        total_mass=1000000.0,
        collector_area=500000.0,
        construction_time=180.0,
        launch_mass_rate=1000.0,
        target_capture_percent=85.0,
        num_swarms=10,
        swarm_size=100,
        replication_factor=1.5,
        maintenance_factor=0.8,
        energy_efficiency=90.0,
        resource_efficiency=85.0,
        simulation_duration=365,
        launch_systems=["SystemA", "SystemB"],
        mass_allocation={"component1": 500000.0, "component2": 500000.0}
    )
    assert results.total_mass == 1000000.0
    assert results.launch_systems == ["SystemA", "SystemB"]

def test_simulation_results_invalid_total_mass():
    with pytest.raises(ValueError, match="Total mass cannot be negative"):
        SimulationResults(
            total_mass=-1000.0,
            collector_area=500000.0,
            construction_time=180.0,
            launch_mass_rate=1000.0,
            target_capture_percent=85.0,
            num_swarms=10,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0,
            simulation_duration=365
        )

def test_simulation_results_invalid_collector_area():
    with pytest.raises(ValueError, match="Collector area cannot be negative"):
        SimulationResults(
            total_mass=1000000.0,
            collector_area=-500000.0,
            construction_time=180.0,
            launch_mass_rate=1000.0,
            target_capture_percent=85.0,
            num_swarms=10,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0,
            simulation_duration=365
        )

def test_simulation_results_invalid_construction_time():
    with pytest.raises(ValueError, match="Construction time cannot be negative"):
        SimulationResults(
            total_mass=1000000.0,
            collector_area=500000.0,
            construction_time=-180.0,
            launch_mass_rate=1000.0,
            target_capture_percent=85.0,
            num_swarms=10,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0,
            simulation_duration=365
        )

def test_simulation_results_invalid_launch_systems_type():
    with pytest.raises(ValueError, match="Launch systems must be a list"):
        SimulationResults(
            total_mass=1000000.0,
            collector_area=500000.0,
            construction_time=180.0,
            launch_mass_rate=1000.0,
            target_capture_percent=85.0,
            num_swarms=10,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0,
            simulation_duration=365,
            launch_systems="invalid_type"
        )

def test_simulation_results_invalid_mass_allocation_type():
    with pytest.raises(ValueError, match="Mass allocation must be a dictionary"):
        SimulationResults(
            total_mass=1000000.0,
            collector_area=500000.0,
            construction_time=180.0,
            launch_mass_rate=1000.0,
            target_capture_percent=85.0,
            num_swarms=10,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0,
            simulation_duration=365,
            mass_allocation="invalid_type"
        )

def test_simulation_results_negative_num_swarms():
    with pytest.raises(ValueError, match="Number of swarms cannot be negative"):
        SimulationResults(
            total_mass=1000000.0,
            collector_area=500000.0,
            construction_time=180.0,
            launch_mass_rate=1000.0,
            target_capture_percent=85.0,
            num_swarms=-5,
            swarm_size=100,
            replication_factor=1.5,
            maintenance_factor=0.8,
            energy_efficiency=90.0,
            resource_efficiency=85.0,
            simulation_duration=365
        )

def test_simulation_results_default_launch_systems_and_mass_allocation():
    results = SimulationResults(
        total_mass=1000000.0,
        collector_area=500000.0,
        construction_time=180.0,
        launch_mass_rate=1000.0,
        target_capture_percent=85.0,
        num_swarms=10,
        swarm_size=100,
        replication_factor=1.5,
        maintenance_factor=0.8,
        energy_efficiency=90.0,
        resource_efficiency=85.0,
        simulation_duration=365
    )
    assert results.launch_systems == []
    assert results.mass_allocation == {}