import dataclasses
from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np

@dataclass
class SimulationParameters:
    target_capture_percent: float
    launch_mass_rate: float
    simulation_duration: int
    num_swarms: int
    swarm_size: int
    replication_factor: float
    maintenance_factor: float
    energy_efficiency: float
    resource_efficiency: float
    
    def __post_init__(self):
        # Validation for target_capture_percent
        if not 0 <= self.target_capture_percent <= 100:
            raise ValueError("Target capture percentage must be between 0 and 100")
        
        # Validation for launch_mass_rate
        if self.launch_mass_rate <= 0:
            raise ValueError("Launch mass rate must be positive")
            
        # Validation for simulation_duration
        if self.simulation_duration <= 0:
            raise ValueError("Simulation duration must be positive")
        
        # Validation for num_swarms
        if self.num_swarms <= 0:
            raise ValueError("Number of swarms must be positive")
            
        # Validation for swarm_size
        if self.swarm_size <= 0:
            raise ValueError("Swarm size must be positive")
            
        # Validation for replication_factor
        if self.replication_factor <= 0:
            raise ValueError("Replication factor must be positive")
            
        # Validation for maintenance_factor
        if self.maintenance_factor <= 0:
            raise ValueError("Maintenance factor must be positive")
            
        # Validation for energy_efficiency
        if not 0 <= self.energy_efficiency <= 100:
            raise ValueError("Energy efficiency must be between 0 and 100")
            
        # Validation for resource_efficiency
        if not 0 <= self.resource_efficiency <= 100:
            raise ValueError("Resource efficiency must be between 0 and 100")

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

@dataclass
class SimulationResults:
    total_mass: float
    collector_area: float
    construction_time: float
    launch_mass_rate: float
    target_capture_percent: float
    num_swarms: int
    swarm_size: int
    replication_factor: float
    maintenance_factor: float
    energy_efficiency: float
    resource_efficiency: float
    simulation_duration: int
    launch_systems: List[str] = dataclasses.field(default_factory=list)
    mass_allocation: Dict[str, float] = dataclasses.field(default_factory=dict)
    
    def __post_init__(self):
        # Validation for total_mass
        if self.total_mass < 0:
            raise ValueError("Total mass cannot be negative")
        
        # Validation for collector_area
        if self.collector_area < 0:
            raise ValueError("Collector area cannot be negative")
            
        # Validation for construction_time
        if self.construction_time < 0:
            raise ValueError("Construction time cannot be negative")
            
        # Validation for launch_mass_rate
        if self.launch_mass_rate < 0:
            raise ValueError("Launch mass rate cannot be negative")
            
        # Validation for target_capture_percent
        if self.target_capture_percent < 0:
            raise ValueError("Target capture percent cannot be negative")
            
        # Validation for num_swarms
        if self.num_swarms < 0:
            raise ValueError("Number of swarms cannot be negative")
            
        # Validation for swarm_size
        if self.swarm_size < 0:
            raise ValueError("Swarm size cannot be negative")
            
        # Validation for replication_factor
        if self.replication_factor < 0:
            raise ValueError("Replication factor cannot be negative")
            
        # Validation for maintenance_factor
        if self.maintenance_factor < 0:
            raise ValueError("Maintenance factor cannot be negative")
            
        # Validation for energy_efficiency
        if self.energy_efficiency < 0:
            raise ValueError("Energy efficiency cannot be negative")
            
        # Validation for resource_efficiency
        if self.resource_efficiency < 0:
            raise ValueError("Resource efficiency cannot be negative")
            
        # Validation for simulation_duration
        if self.simulation_duration < 0:
            raise ValueError("Simulation duration cannot be negative")
            
        # Validation for launch_systems
        if not isinstance(self.launch_systems, list):
            raise ValueError("Launch systems must be a list")
            
        # Validation for mass_allocation
        if not isinstance(self.mass_allocation, dict):
            raise ValueError("Mass allocation must be a dictionary")