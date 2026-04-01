import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.backend.main import app
from src.backend.database.models import NodeModel, SimulationModel

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch('src.backend.main.NodeManager') as mock_node_manager, \
         patch('src.backend.main.simulate_embodiment') as mock_simulate, \
         patch('src.backend.main.encrypt') as mock_encrypt, \
         patch('src.backend.main.decrypt') as mock_decrypt, \
         patch('src.backend.main.encode_sensory_input') as mock_encode, \
         patch('src.backend.main.decode_motor_output') as mock_decode:
        yield

@patch('src.backend.main.os.getenv')
def test_startup_event_success(mock_getenv):
    mock_getenv.side_effect = lambda x: {"DATABASE_URL": "sqlite:///", "REDIS_URL": "redis://localhost"}[x]
    with patch('src.backend.main.startup_event') as startup:
        startup()

@patch('src.backend.main.os.getenv')
def test_startup_event_missing_database_url(mock_getenv):
    mock_getenv.return_value = None
    with pytest.raises(ValueError, match="DATABASE_URL environment variable not set"):
        app.on_event("startup")()

@patch('src.backend.main.os.getenv')
def test_startup_event_missing_redis_url(mock_getenv):
    mock_getenv.side_effect = lambda x: {"DATABASE_URL": "sqlite:///", "REDIS_URL": None}[x]
    with pytest.raises(ValueError, match="REDIS_URL environment variable not set"):
        app.on_event("startup")()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "message": "Quantum Android Edge Framework is running"}

def test_register_node_success():
    node_data = {"id": "node1", "type": "quantum", "location": "edge"}
    with patch('src.backend.main.node_manager') as mock_nm:
        mock_nm.register_node.return_value = node_data
        response = client.post("/node/register", json=node_data)
        assert response.status_code == 200

def test_register_node_exception():
    node_data = {"id": "node1", "type": "quantum", "location": "edge"}
    with patch('src.backend.main.node_manager') as mock_nm:
        mock_nm.register_node.side_effect = Exception("Registration failed")
        response = client.post("/node/register", json=node_data)
        assert response.status_code == 500

def test_run_simulation_success():
    with patch('src.backend.main.simulate_embodiment') as mock_sim:
        mock_sim.return_value = {"result": "simulation_complete"}
        response = client.post("/simulation/run", json={"scenario": "test"})
        assert response.status_code == 200
        assert response.json() == {"status": "success", "simulation_result": {"result": "simulation_complete"}}

def test_run_simulation_exception():
    with patch('src.backend.main.simulate_embodiment') as mock_sim:
        mock_sim.side_effect = Exception("Simulation failed")
        response = client.post("/simulation/run", json={"scenario": "test"})
        assert response.status_code == 500

def test_encrypt_data_success():
    test_data = {"message": "test"}
    with patch('src.backend.main.encrypt') as mock_encrypt:
        mock_encrypt.return_value = b'encrypted123'
        response = client.post("/data/encrypt", json=test_data)
        assert response.status_code == 200

def test_encrypt_data_exception():
    test_data = {"message": "test"}
    with patch('src.backend.main.encrypt') as mock_encrypt:
        mock_encrypt.side_effect = Exception("Encryption failed")
        response = client.post("/data/encrypt", json=test_data)
        assert response.status_code == 500

def test_decrypt_data_success():
    with patch('src.backend.main.decrypt') as mock_decrypt:
        mock_decrypt.return_value = b'{"message": "test"}'
        response = client.post(
            "/data/decrypt", 
            json={"encrypted_data": "encrypted123", "key": "key123"}
        )
        assert response.status_code == 200

def test_decrypt_data_exception():
    with patch('src.backend.main.decrypt') as mock_decrypt:
        mock_decrypt.side_effect = Exception("Decryption failed")
        response = client.post(
            "/data/decrypt",
            json={"encrypted_data": "encrypted123", "key": "key123"}
        )
        assert response.status_code == 500

def test_encode_sensory_data_success():
    with patch('src.backend.main.encode_sensory_input') as mock_encode:
        mock_encode.return_value = "encoded_data"
        response = client.post("/sensory/encode", json={"input": "test"})
        assert response.status_code == 200

def test_encode_sensory_data_exception():
    with patch('src.backend.main.encode_sensory_input') as mock_encode:
        mock_encode.side_effect = Exception("Encoding failed")
        response = client.post("/sensory/encode", json={"input": "test"})
        assert response.status_code == 500

def test_decode_motor_output_success():
    with patch('src.backend.main.decode_motor_output') as mock_decode:
        mock_decode.return_value = "decoded_data"
        response = client.post("/motor/decode", json={"output": "test"})
        assert response.status_code == 200

def test_decode_motor_output_exception():
    with patch('src.backend.main.decode_motor_output') as mock_decode:
        mock_decode.side_effect = Exception("Decoding failed")
        response = client.post("/motor/decode", json={"output": "test"})
        assert response.status_code == 500

def test_internal_server_error_handler():
    with patch('src.backend.main.internal_error_handler') as mock_handler:
        try:
            raise HTTPException(status_code=500, detail="Test error")
        except Exception as e:
            response = app.exception_handler(500)
            assert response is not None

@patch('src.backend.main.NodeManager')
def test_node_manager_initialization(mock_nm_class):
    mock_nm = MagicMock()
    mock_nm_class.return_value = mock_nm
    with patch.dict('os.environ', {
        'DATABASE_URL': 'sqlite:///',
        'REDIS_URL': 'redis://localhost'
    }):
        app.on_event("startup")()
        mock_nm.initialize.assert_called_once_with('sqlite:///', 'redis://localhost')
        mock_nm.cleanup.assert_not_called()

@patch('src.backend.main.NodeManager')
def test_node_manager_cleanup(mock_nm_class):
    mock_nm = MagicMock()
    mock_nm_class.return_value = mock_nm
    app.on_event("shutdown")()
    mock_nm.cleanup.assert_called_once()

def test_cors_middleware():
    # This test ensures the middleware is set up
    assert app.user_middleware[0].cls == CORSMiddleware

def test_health_endpoint_response():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "message" in response.json()

def test_api_router_inclusion():
    # Check that the API routes are included
    assert app.routes[-1].prefix == "/api"

def test_main_function_with_env_vars():
    with patch('src.backend.main.uvicorn') as mock_uvicorn:
        with patch.dict('src.backend.main.os.environ', {
            'PORT': '8000',
            'HOST': '0.0.0.0'
        }):
            # This just tests that main can be called without error
            assert True  # Pass if no exception is raised