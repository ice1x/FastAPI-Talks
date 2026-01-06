"""
REST API Requester Service

This service benchmarks standard REST API communication with JSON serialization.
It sends 1,000 HTTP requests with JSON payloads and measures response times
for performance analysis.
"""

import sys
from pathlib import Path

# Add parent directory to path for common imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
from common import BaseBenchmarkRequester, BenchmarkConfig


class RestRequester(BaseBenchmarkRequester):
    """REST API benchmark requester using JSON serialization."""

    def __init__(self):
        """Initialize REST requester with configuration."""
        config = BenchmarkConfig(
            protocol_name="REST",
            responder_port=8000,
            requester_port=8080,
        )
        super().__init__(config)

    async def _send_request(
        self, client: httpx.AsyncClient, request_timestamp: str
    ) -> dict:
        """
        Send a single REST API request with JSON payload.

        Args:
            client: HTTP client for connection pooling
            request_timestamp: Request timestamp to send

        Returns:
            Dictionary with request and response timestamps
        """
        url = f"{self.config.responder_url}/timestamp"
        payload = {"request_timestamp": request_timestamp}

        response = await client.post(
            url, json=payload, timeout=self.config.timeout
        )
        response.raise_for_status()

        return response.json()

    def _get_health_response(self) -> dict:
        """Customize health check response for REST."""
        return {
            "service": "REST API Requester",
            "status": "running",
            "format": "JSON over HTTP",
            "endpoint": "/run-benchmark",
        }


# Create requester instance and expose app
requester = RestRequester()
app = requester.app
