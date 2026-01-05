"""
Tests for GraphQL services.
"""

import pytest
from fastapi.testclient import TestClient
from graphql_responder.main import app as responder_app
from datetime import datetime


class TestGraphQLResponder:
    """Test GraphQL responder functionality."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(responder_app)

    def test_root_endpoint(self, client):
        """Test that root endpoint returns service info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "GraphQL Responder"
        assert data["status"] == "running"

    def test_graphql_endpoint_exists(self, client):
        """Test that GraphQL endpoint is available."""
        # GraphQL typically responds to POST requests
        query = """
        query {
            __schema {
                types {
                    name
                }
            }
        }
        """
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200

    def test_get_timestamps_query(self, client):
        """Test the getTimestamps query."""
        query = """
        query getTimestamps($requestTimestamp: DateTime!) {
            getTimestamps(requestTimestamp: $requestTimestamp) {
                requestTimestamp
                responseTimestamp
            }
        }
        """
        variables = {"requestTimestamp": datetime.utcnow().isoformat()}
        response = client.post("/graphql", json={"query": query, "variables": variables})
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "getTimestamps" in data["data"]
