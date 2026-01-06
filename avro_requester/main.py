"""
AVRO Requester Service

This service benchmarks Apache Avro binary serialization format.
It sends 1,000 HTTP requests with Avro-serialized payloads and measures
response times for performance analysis.
"""

import io
import sys
from pathlib import Path

# Add parent directory to path for common imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import avro.io
import avro.schema
import httpx

from common import BaseBenchmarkRequester, BenchmarkConfig, TIMESTAMP_SCHEMA_AVRO


class AvroRequester(BaseBenchmarkRequester):
    """AVRO benchmark requester using binary serialization."""

    def __init__(self):
        """Initialize AVRO requester with schema."""
        config = BenchmarkConfig(
            protocol_name="AVRO",
            responder_port=8000,
            requester_port=8080,
        )
        super().__init__(config)

        # Parse AVRO schema
        self.schema = avro.schema.parse(TIMESTAMP_SCHEMA_AVRO)

    async def _send_request(
        self, client: httpx.AsyncClient, request_timestamp: str
    ) -> dict:
        """
        Send a single Avro-serialized request.

        Args:
            client: HTTP client for connection pooling
            request_timestamp: Request timestamp to send

        Returns:
            Dictionary with request and response timestamps
        """
        url = f"{self.config.responder_url}/timestamp"

        # Serialize request with Avro
        writer = avro.io.DatumWriter(self.schema)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write(
            {"request_timestamp": request_timestamp, "response_timestamp": ""},
            encoder,
        )

        # Send request
        response = await client.post(
            url,
            content=bytes_writer.getvalue(),
            headers={"Content-Type": "application/avro"},
            timeout=self.config.timeout,
        )
        response.raise_for_status()

        # Deserialize response
        reader = avro.io.DatumReader(self.schema)
        bytes_reader = io.BytesIO(response.content)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        result = reader.read(decoder)

        return result

    def _get_health_response(self) -> dict:
        """Customize health check response for AVRO."""
        return {
            "service": "AVRO Requester",
            "status": "running",
            "format": "Apache Avro Binary",
            "endpoint": "/run-benchmark",
        }


# Create requester instance and expose app
requester = AvroRequester()
app = requester.app
