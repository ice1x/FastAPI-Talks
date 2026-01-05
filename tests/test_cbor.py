"""
Tests for CBOR serialization services.
"""

import pytest
from fastapi.testclient import TestClient

from cbor_responder.main import app as responder_app


class TestCBORResponder:
    """Test CBOR responder functionality."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(responder_app)

    def test_root_endpoint(self, client):
        """Test that root endpoint returns service info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "CBOR Responder"
        assert data["status"] == "running"
        assert "CBOR" in data["format"]

    def test_health_check_has_message(self, client):
        """Test that health check includes ready message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Ready" in data["message"]
