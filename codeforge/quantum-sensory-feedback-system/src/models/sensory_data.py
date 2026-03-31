from pydantic import Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from src.models.quantum_state import QuantumState
from src.models.perception_model import PerceptionModel


class SensoryData(BaseModel):
    """Sensory data model for quantum sensory feedback system"""
    
    # Core data fields
    id: Optional[str] = Field(default=None, description="Unique identifier for the sensory data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of data creation")
    sensor_type: str = Field(..., description="Type of sensor producing the data")
    raw_data: List[float] = Field(..., description="Raw sensory data values")
    source_id: Optional[str] = Field(default=None, description="Source identifier for the sensor")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata about the sensory data")
    
    # Model relationships
    quantum_state: Optional[QuantumState] = Field(default=None, description="Associated quantum state data")
    perception: Optional[PerceptionModel] = Field(default=None, description="Perception model results")
    processed_data: Optional[Dict[str, Any]] = Field(default=None, description="Processed sensory data")
    processing_context: Optional[Dict[str, Any]] = Field(default=None, description="Context for data processing")
    calibration_data: Optional[Dict[str, Any]] = Field(default=None, description="Calibration information")

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary representation"""
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SensoryData':
        """Create SensoryData instance from dictionary"""
        return cls(**data)

    def update_quantum_state(self, quantum_data: Dict[str, Any]) -> None:
        """Update the quantum state with new processing results"""
        # Add missing required fields with default values
        if "state_vector" not in quantum_data:
            quantum_data["state_vector"] = [0.0]
        if "entropy" not in quantum_data:
            quantum_data["entropy"] = 0.0
        self.quantum_state = QuantumState(**quantum_data)

    def update_perception_model(self, perception_data: Dict[str, Any]) -> None:
        """Update perception model with new data"""
        # Add missing required fields with default values
        if "sensory_input" not in perception_data:
            perception_data["sensory_input"] = []
        if "features" not in perception_data:
            perception_data["features"] = {}
        if "quantum_state" not in perception_data:
            perception_data["quantum_state"] = None
        self.perception = PerceptionModel(**perception_data)

    def add_metadata(self, key: str, value: str) -> None:
        """Add metadata to the sensory data"""
        if self.metadata is None:
            self.metadata = {}
        self.metadata[key] = value

    def get_metadata(self, key: str) -> Any:
        """Get metadata value by key"""
        if self.metadata is None:
            return None
        return self.metadata.get(key)

    def __hash__(self) -> int:
        """Make SensoryData hashable"""
        return hash(self.json())