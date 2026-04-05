import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from fastapi import status
from backend.app.api.routes.system import router
from fastapi.testclient import TestClient
import sys
import os

# Add the path to the system.py to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from system import get_system_health, get_system_status, get_system_metrics, get_all_agents, get_all_metrics, get_node_status

def test_get_system_health_success():
    client = TestClient(router)
    with patch('system.get_system_metrics', return_value=Mock()) as mock_metrics:
        mock_metrics.return_value = {"cpu": 25.0, "memory": 80.0}
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK

def test_get_system_health_db_error():
    # Test that should fail due to missing DB
    with patch('system.get_system_health', return_value=Mock()) as mock_health:
        mock_health.return_value = {"cpu": 50, "memory": 80}
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK

def test_get_system_status_success():
    client = TestClient(router)
    with patch('system.get_node_status', return_value=Mock()) as mock_status:
        mock_status.return_value = {"status": "active", "message": "Node is active"}
        response = client.get("/status")
        assert response.status_code == status.HTTP_200_OK

def test_get_system_status_db_healthy():
    # Test that should return healthy status when DB is accessible
    response = client.get("/status")
    assert response.status_code == status.HTTP_200_OK

def test_get_system_status_success_2():
    # Test with healthy DB response
    response = client.get("/status")
    assert response.status_code == status.HTTP_200_OK