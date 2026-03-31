from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import numpy as np
from datetime import datetime


class QuantumState(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the quantum state")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of quantum state creation")
    state_vector: List[complex] = Field(..., description="Quantum state vector representation")
    entropy: float = Field(..., description="Quantum entropy measurement")
    coherence: float = Field(..., description="Quantum coherence level")
    entanglement: float = Field(..., description="Quantum entanglement degree")
    amplitude: Optional[float] = Field(None, description="Quantum amplitude value")
    phase: Optional[float] = Field(None, description="Quantum phase angle")
    frequency: Optional[float] = Field(None, description="Quantum state frequency")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Quantum configuration parameters")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the quantum state")

    class Config:
        schema_extra = {
            "example": {
                "state_vector": [complex(1, 0), complex(0, 1)],
                "entropy": 0.5,
                "coherence": 0.8,
                "entanglement": 0.3,
                "amplitude": 1.0,
                "phase": 0.0,
                "frequency": 100.0,
                "configuration": {
                    "qubits": 2,
                    "gates": ["H", "CNOT"]
                },
                "metadata": {
                    "source": "sensory_input",
                    "version": "1.0"
                }
            }
        }