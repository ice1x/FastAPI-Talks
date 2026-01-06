"""
GraphQL Requester Service

This service acts as a benchmark client for the GraphQL responder.
It sends 1,000 GraphQL queries and collects response timestamps
for performance analysis.
"""

import sys
from pathlib import Path

# Add parent directory to path for common imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx

from common import BaseBenchmarkRequester, BenchmarkConfig


class GraphqlRequester(BaseBenchmarkRequester):
    """GraphQL benchmark requester using GraphQL queries."""

    # GraphQL query template
    GRAPHQL_QUERY = """
    query getTimestamps($requestTimestamp: DateTime!) {
      getTimestamps(requestTimestamp: $requestTimestamp) {
        requestTimestamp
        responseTimestamp
      }
    }
    """

    def __init__(self):
        """Initialize GraphQL requester with configuration."""
        config = BenchmarkConfig(
            protocol_name="GraphQL",
            responder_port=8000,
            requester_port=8080,
        )
        super().__init__(config)

    async def _send_request(
        self, client: httpx.AsyncClient, request_timestamp: str
    ) -> dict:
        """
        Send a single GraphQL query request.

        Args:
            client: HTTP client for connection pooling
            request_timestamp: Request timestamp to send

        Returns:
            Dictionary with request and response timestamps
        """
        url = f"{self.config.responder_url}/graphql"

        payload = {
            "query": self.GRAPHQL_QUERY,
            "variables": {"requestTimestamp": request_timestamp},
        }

        response = await client.post(
            url,
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()

        data = response.json()
        return data["data"]["getTimestamps"]

    def _get_health_response(self) -> dict:
        """Customize health check response for GraphQL."""
        return {
            "service": "GraphQL Requester",
            "status": "running",
            "format": "GraphQL with Strawberry",
            "endpoint": "/run-benchmark",
        }


# Create requester instance and expose app
requester = GraphqlRequester()
app = requester.app
