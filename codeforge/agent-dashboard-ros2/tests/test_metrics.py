from unittest.mock import patch, MagicMock
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient


# Create a test client instance
client = TestClient(pytest.importorskip("backend.app.api.routes.metrics").router)


def test_get_metrics_success():
    with patch("backend.app.api.routes.metrics.get_all_metrics") as mock_get_all_metrics:
        mock_get_all_metrics.return_value = []
        response = client.get("/metrics")
        assert response.status_code == 200


def test_get_metrics_exception():
    with patch("backend.app.api.routes.metrics.get_all_metrics") as mock_get_all_metrics:
        mock_get_all_metrics.side_effect = Exception("Database error")
        response = client.get("/metrics")
        assert response.status_code == 500
        assert "Database error" in response.json()["detail"]


def test_get_agent_metrics_success():
    with patch("backend.app.api.routes.metrics.get_metrics_for_agent") as mock_get_metrics:
        mock_get_metrics.return_value = []
        response = client.get("/metrics/agent/1")
        assert response.status_code == 200


def test_get_agent_metrics_not_found():
    with patch("backend.app.api.routes.metrics.get_metrics_for_agent") as mock_get_metrics:
        mock_get_metrics.return_value = []
        response = client.get("/metrics/agent/999")
        assert response.status_code == 404


def test_get_agent_metrics_exception():
    with patch("backend.app.api.routes.metrics.get_metrics_for_agent") as mock_get_metrics:
        mock_get_metrics.side_effect = Exception("Service error")
        response = client.get("/metrics/agent/1")
        assert response.status_code == 500


def test_get_agent_metrics_service_error():
    with patch("backend.app.api.routes.metrics.get_metrics_for_agent") as mock_get_metrics:
        mock_get_metrics.side_effect = Exception("Service error")
        response = client.get("/metrics/agent/1")
        assert response.status_code == 500
        assert "Service error" in response.json()["detail"]


def test_post_metrics_success():
    fake_metric_data = {
        "agent_id": 1,
        "timestamp": "2023-01-01T00:00:00",
        "value": 1.23
    }
    with patch("backend.app.api.routes.metrics.create_metric_service") as mock_create:
        mock_metric = MagicMock()
        mock_metric.agent_id = 1
        mock_metric.timestamp = "2023-01-01T00:00:00"
        mock_metric.value = 1.23
        mock_create.return_value = mock_metric
        response = client.post("/metrics", json=fake_metric_data)
        assert response.status_code == 201


def test_post_metrics_exception():
    fake_metric_data = {
        "agent_id": 1,
        "timestamp": "2023-01-01T00:00:00",
        "value": 1.23
    }
    with patch("backend.app.api.routes.metrics.create_metric_service") as mock_create:
        mock_create.side_effect = Exception("Creation failed")
        response = client.post("/metrics", json=fake_metric_data)
        assert response.status_code == 500


def test_post_metrics_validation_error():
    response = client.post("/metrics", json={"invalid": "data"})
    assert response.status_code == 422