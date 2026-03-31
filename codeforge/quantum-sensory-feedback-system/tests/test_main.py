import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import (
    create_app,
    SensoryData,
    quantum_fourier_transform,
    process_signal,
    SensoryInputHandler,
    QuantumProcessor,
    OrchOREngine,
    PerceptionAdaptation,
    PatternRecognition,
    ActuatorController,
    ResponseGenerator
)
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "Quantum Sensory Feedback System"}

def test_process_sensory_data_success(client):
    test_data = {"data": {"sensor1": 1.5, "sensor2": 2.3}}
    response = client.post("/process", json=test_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_process_sensory_data_invalid_input(client):
    response = client.post("/process", json={"invalid": "data"})
    assert response.status_code == 422

def test_quantum_fourier_transform_stub():
    data = [1, 2, 3, 4]
    result = quantum_fourier_transform(data)
    assert result == data

def test_process_signal_stub():
    signal = [1, 2, 3, 4]
    result = process_signal(signal)
    assert result == signal

def test_sensory_input_handler_process():
    handler = SensoryInputHandler()
    input_data = {"test": "data"}
    result = handler.process_input(input_data)
    assert result == input_data

def test_quantum_processor_process():
    processor = QuantumProcessor()
    input_data = {"value": 42}
    result = processor.process_quantum_state(input_data)
    assert result == input_data

def test_orch_or_engine_compute():
    engine = OrchOREngine()
    input_data = {"quantum": "state"}
    result = engine.compute_orch_or_state(input_data)
    assert result == input_data

def test_perception_adaptation_adapt():
    adaptation = PerceptionAdaptation()
    input_data = {"sensor": "input"}
    result = adaptation.adapt_to_input(input_data)
    assert result == input_data

def test_pattern_recognition_recognize():
    recognizer = PatternRecognition()
    test_data = [{"pattern": "test"}]
    result = recognizer.recognize_patterns(test_data)
    assert result == test_data

def test_actuator_controller_control():
    controller = ActuatorController()
    input_data = {"control": "signal"}
    result = controller.control_response(input_data)
    assert result == input_data

def test_response_generator_generate():
    generator = ResponseGenerator()
    input_data = {"processed": "data"}
    result = generator.generate_feedback(input_data)
    assert result == input_data

def test_sensory_data_model():
    data = {"sensor1": 1.0, "sensor2": 2.0}
    sensory_data = SensoryData(data=data)
    assert sensory_data.data == data

def test_sensory_data_model_empty():
    sensory_data = SensoryData()
    assert sensory_data.data == {}

def test_sensory_data_model_invalid_type():
    with pytest.raises(ValueError):
        SensoryData(data="invalid")

def test_process_endpoint_exception(client):
    with patch('src.main.SensoryInputHandler.process_input', side_effect=Exception("Test error")):
        response = client.post("/process", json={"data": {}})
        assert response.status_code == 500

def test_process_endpoint_empty_data(client):
    response = client.post("/process", json={})
    assert response.status_code == 422

def test_process_endpoint_missing_data_field(client):
    response = client.post("/process", json={"other_field": "value"})
    assert response.status_code == 422

def test_process_endpoint_with_complex_data(client):
    complex_data = {
        "data": {
            "temperature": 23.5,
            "humidity": 45.0,
            "pressure": 1013.25
        }
    }
    response = client.post("/process", json=complex_data)
    assert response.status_code == 200
    assert "status" in response.json()

def test_process_endpoint_data_integrity(client):
    test_data = {"data": {"input": "test"}}
    response = client.post("/process", json=test_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "success"
    assert "data" in response_json
    assert response_json["data"] == test_data["data"]