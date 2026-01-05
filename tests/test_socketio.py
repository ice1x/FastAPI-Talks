"""
Tests for Socket.IO services.
"""

import pytest
from fastapi.testclient import TestClient
from sio_responder.main import app as responder_app


class TestSocketIOResponder:
    """Test Socket.IO responder functionality."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(responder_app)

    def test_root_endpoint(self, client):
        """Test that root endpoint returns service info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Socket.IO Responder"
        assert data["status"] == "running"

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Socket.IO" in response.text
