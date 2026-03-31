import pytest
from datetime import datetime
from src.models.quantum_state import QuantumState


def test_quantum_state_creation():
    state = QuantumState(
        state_vector=[complex(1, 0), complex(0, 1)],
        entropy=0.5,
        coherence=0.8,
        entanglement=0.3
    )
    assert state.state_vector == [complex(1, 0), complex(0, 1)]
    assert state.entropy == 0.5
    assert state.coherence == 0.8
    assert state.entanglement == 0.3


def test_quantum_state_with_optional_fields():
    state = QuantumState(
        state_vector=[complex(1, 0)],
        entropy=0.5,
        coherence=0.8,
        entanglement=0.3,
        amplitude=1.0,
        phase=0.0,
        frequency=100.0
    )
    assert state.amplitude == 1.0
    assert state.phase == 0.0
    assert state.frequency == 100.0


def test_quantum_state_with_id():
    state = QuantumState(
        id="test-id",
        state_vector=[complex(1, 0)],
        entropy=0.5,
        coherence=0.8,
        entanglement=0.3
    )
    assert state.id == "test-id"


def test_quantum_state_with_configuration():
    config = {"qubits": 2, "gates": ["H", "CNOT"]}
    state = QuantumState(
        state_vector=[complex(1, 0)],
        entropy=0.5,
        coherence=0.8,
        entanglement=0.3,
        configuration=config
    )
    assert state.configuration == config


def test_quantum_state_with_metadata():
    metadata = {"source": "sensory_input", "version": "1.0"}
    state = QuantumState(
        state_vector=[complex(1, 0)],
        entropy=0.5,
        coherence=0.8,
        entanglement=0.3,
        metadata=metadata
    )
    assert state.metadata == metadata


def test_quantum_state_timestamp_created_automatically():
    state = QuantumState(
        state_vector=[complex(1, 0)],
        entropy=0.5,
        coherence=0.8,
        entanglement=0.3
    )
    assert isinstance(state.timestamp, datetime)


def test_quantum_state_invalid_state_vector_type():
    with pytest.raises(Exception):
        QuantumState(
            state_vector="invalid",
            entropy=0.5,
            coherence=0.8,
            entanglement=0.3
        )


def test_quantum_state_missing_required_fields():
    with pytest.raises(Exception):
        QuantumState()


def test_quantum_state_invalid_entropy_type():
    with pytest.raises(Exception):
        QuantumState(
            state_vector=[complex(1, 0)],
            entropy="invalid",
            coherence=0.8,
            entanglement=0.3
        )


def test_quantum_state_invalid_coherence_type():
    with pytest.raises(Exception):
        QuantumState(
            state_vector=[complex(1, 0)],
            entropy=0.5,
            coherence="invalid",
            entanglement=0.3
        )


def test_quantum_state_invalid_entanglement_type():
    with pytest.raises(Exception):
        QuantumState(
            state_vector=[complex(1, 0)],
            entropy=0.5,
            coherence=0.8,
            entanglement="invalid"
        )


def test_quantum_state_negative_entropy():
    state = QuantumState(
        state_vector=[complex(1, 0)],
        entropy=-0.5,
        coherence=0.8,
        entanglement=0.3
    )
    assert state.entropy == -0.5


def test_quantum_state_negative_coherence():
    state = QuantumState(
        state_vector=[complex(1, 0)],
        entropy=0.5,
        coherence=-0.8,
        entanglement=0.3
    )
    assert state.coherence == -0.8


def test_quantum_state_negative_entanglement():
    state = QuantumState(
        state_vector=[complex(1, 0)],
        entropy=0.5,
        coherence=0.8,
        entanglement=-0.3
    )
    assert state.entanglement == -0.3


def test_quantum_state_empty_state_vector():
    state = QuantumState(
        state_vector=[],
        entropy=0.5,
        coherence=0.8,
        entanglement=0.3
    )
    assert state.state_vector == []


def test_quantum_state_complex_state_vector():
    state = QuantumState(
        state_vector=[complex(0, 0), complex(0, 1), complex(1, 1)],
        entropy=0.5,
        coherence=0.8,
        entanglement=0.3
    )
    assert len(state.state_vector) == 3
    assert state.state_vector[1] == complex(0, 1)
    assert state.state_vector[2] == complex(1, 1)


def test_quantum_state_none_optional_fields():
    state = QuantumState(
        state_vector=[complex(1, 0)],
        entropy=0.5,
        coherence=0.8,
        entanglement=0.3
    )
    assert state.amplitude is None
    assert state.phase is None
    assert state.frequency is None


def test_quantum_state_default_configuration():
    state = QuantumState(
        state_vector=[complex(1, 0)],
        entropy=0.5,
        coherence=0.8,
        entanglement=0.3
    )
    assert state.configuration == {}


def test_quantum_state_default_metadata():
    state = QuantumState(
        state_vector=[complex(1, 0)],
        entropy=0.5,
        coherence=0.8,
        entanglement=0.3
    )
    assert state.metadata == {}