"""
Tests for REST API services.
"""

import pytest
from fastapi.testclient import TestClient
from rest_responder.main import app as responder_app, TimestampRequest


class TestRESTResponder:
    """Test REST API responder functionality."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(responder_app)

    def test_root_endpoint(self, client):
        """Test that root endpoint returns service info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "REST API Responder"
        assert data["status"] == "running"
        assert data["format"] == "JSON over HTTP"

    def test_timestamp_endpoint_success(self, client):
        """Test successful timestamp request."""
        payload = {"request_timestamp": "2024-01-01T00:00:00"}
        response = client.post("/timestamp", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "request_timestamp" in data
        assert "response_timestamp" in data
        assert data["request_timestamp"] == "2024-01-01T00:00:00"

    def test_timestamp_endpoint_validation(self, client):
        """Test that invalid requests are rejected."""
        # Missing request_timestamp
        response = client.post("/timestamp", json={})
        assert response.status_code == 422  # Validation error

    def test_timestamp_endpoint_returns_valid_response(self, client):
        """Test that response timestamp is valid."""
        from datetime import datetime

        payload = {"request_timestamp": datetime.now().isoformat()}
        response = client.post("/timestamp", json=payload)

        assert response.status_code == 200
        data = response.json()
        # Verify response_timestamp is a valid ISO format
        datetime.fromisoformat(data["response_timestamp"])

    def test_health_check_has_message(self, client):
        """Test that health check includes ready message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Ready" in data["message"]
