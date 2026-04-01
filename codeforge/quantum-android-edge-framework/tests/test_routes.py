import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.backend.api.routes import router
from fastapi import FastAPI

# Create a FastAPI app and include the router for testing
app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "quantum-android-edge-framework"}

def test_create_node_success():
    with patch("src.backend.api.routes.NodeManager.create_node") as mock_create:
        mock_create.return_value = MagicMock(node_id="node123")
        response = client.post("/nodes/create", json={"node_id": "test_node", "config": {}})
        assert response.status_code == 200
        # Should return {"node_id": "node123", "status": "created"}

def test_create_node_failure():
    response = client.post("/nodes/create", json={"node_id": "fail_node", "config": {}})
    assert response.status_code == 500

def test_encrypt_node_data_success():
    with patch("src.backend.api.routes.encrypt") as mock_encrypt:
        mock_encrypt.return_value = b'encrypted_data'
        response = client.post("/nodes/node123/encrypt", json={"data": b"test_data"})
        assert response.status_code == 200

def test_encrypt_node_data_failure():
    response = client.post("/nodes/node123/encrypt", json={"data": b"test_data"})
    assert response.status_code == 500

def test_transfer_awareness_success():
    with patch("src.backend.api.routes.transfer_awareness") as mock_transfer:
        mock_transfer.return_value = True
        response = client.post("/nodes/transfer?source_node_id=src&target_node_id=tgt")
        assert response.status_code == 200

def test_transfer_awareness_failure():
    response = client.post("/nodes/transfer?source_node_id=src&target_node_id=tgt")
    assert response.status_code == 500

def test_run_simulation_success():
    with patch("src.backend.api.routes.simulate_embodiment") as mock_sim:
        mock_sim.return_value = {"result": "sim_complete"}
        response = client.post("/simulation/run", json={"scenario": "test", "parameters": {}})
        assert response.status_code == 200

def test_run_simulation_failure():
    response = client.post("/simulation/run", json={"scenario": "invalid", "parameters": {}})
    assert response.status_code == 500

def test_process_sensors_success():
    with patch("src.backend.sensors.processing.process_sensor_data") as mock_proc, \
         patch("src.backend.sensors.processing.filter_noise") as mock_filter:
        mock_proc.return_value = MagicMock()
        mock_filter.return_value = "filtered"
        response = client.post("/sensors/process", json={"raw_sensor_data": b"raw"})
        assert response.status_code == 200

def test_process_sensors_failure():
    response = client.post("/sensors/process", json={"raw_sensor_data": b"invalid"})
    assert response.status_code == 500

def test_maintain_system_state_success():
    with patch("src.backend.iit.continuity.maintain_continuity") as mock_continuity:
        mock_continuity.return_value = "continuity_maintained"
        response = client.post("/state/maintain", json={"state_vector": {}})
        assert response.status_code == 200

def test_maintain_system_state_failure():
    response = client.post("/state/maintain", json={"state_vector": "invalid"})
    assert response.status_code == 500

def test_encode_sensory_success():
    with patch("src.backend.codonic.encoding.encode_sensory_input") as mock_encode:
        mock_encode.return_value = "encoded"
        response = client.post("/encode/sensory", json={"input": "sensory"})
        assert response.status_code == 200

def test_encode_sensory_failure():
    response = client.post("/encode/sensory", json={"input": "invalid"})
    assert response.status_code == 500

def test_decode_motor_success():
    with patch("src.backend.codonic.encoding.decode_motor_output") as mock_decode:
        mock_decode.return_value = "decoded"
        response = client.post("/decode/motor", json={"output": "motor"})
        assert response.status_code == 200

def test_decode_motor_failure():
    response = client.post("/decode/motor", json={"output": "invalid"})
    assert response.status_code == 500

def test_get_nodes_status_success():
    response = client.get("/nodes/status")
    assert response.status_code == 200

def test_get_nodes_status_failure():
    response = client.get("/nodes/status")
    assert response.status_code == 500

def test_node_configuration_success():
    response = client.post("/nodes/test_node/configure", json={"node_id": "test_node", "config": {}})
    assert response.status_code == 200

def test_node_configuration_failure():
    response = client.post("/nodes/invalid/configure")
    assert response.status_code == 404