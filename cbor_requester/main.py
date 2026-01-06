"""
CBOR Requester Service

This service benchmarks CBOR (Concise Binary Object Representation) format.
It sends 1,000 HTTP requests with CBOR-encoded payloads and measures
response times for performance analysis.
"""

import sys
from pathlib import Path

# Add parent directory to path for common imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import cbor2
import httpx

from common import BaseBenchmarkRequester, BenchmarkConfig


class CborRequester(BaseBenchmarkRequester):
    """CBOR benchmark requester using binary encoding."""

    def __init__(self):
        """Initialize CBOR requester with configuration."""
        config = BenchmarkConfig(
            protocol_name="CBOR",
            responder_port=8000,
            requester_port=8080,
        )
        super().__init__(config)

    async def _send_request(
        self, client: httpx.AsyncClient, request_timestamp: str
    ) -> dict:
        """
        Send a single CBOR-encoded request.

        Args:
            client: HTTP client for connection pooling
            request_timestamp: Request timestamp to send

        Returns:
            Dictionary with request and response timestamps
        """
        url = f"{self.config.responder_url}/timestamp"

        # Encode request with CBOR
        payload = cbor2.dumps(
            {"request_timestamp": request_timestamp, "response_timestamp": ""}
        )

        # Send request
        response = await client.post(
            url,
            content=payload,
            headers={"Content-Type": "application/cbor"},
            timeout=self.config.timeout,
        )
        response.raise_for_status()

        # Decode response
        result = cbor2.loads(response.content)
        return result

    def _get_health_response(self) -> dict:
        """Customize health check response for CBOR."""
        return {
            "service": "CBOR Requester",
            "status": "running",
            "format": "CBOR (Concise Binary Object Representation)",
            "endpoint": "/run-benchmark",
        }


# Create requester instance and expose app
requester = CborRequester()
app = requester.app
