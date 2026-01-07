"""
REST API Responder Service

This service provides a standard REST API endpoint that responds to JSON requests.
It receives a timestamp in JSON format and returns it along with the server's
current timestamp.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for common imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import Request, Response
from pydantic import BaseModel

from common import BaseBenchmarkResponder, BenchmarkConfig


class TimestampRequest(BaseModel):
    """Request model for timestamp endpoint."""

    request_timestamp: str


class TimestampResponse(BaseModel):
    """Response model for timestamp endpoint."""

    request_timestamp: str
    response_timestamp: str


class RestResponder(BaseBenchmarkResponder):
    """REST API benchmark responder using JSON serialization."""

    def __init__(self):
        """Initialize REST responder with JSON serializer/deserializer."""
        config = BenchmarkConfig(protocol_name="REST", responder_port=8000)

        # JSON serializer/deserializer
        def serialize(data: dict) -> bytes:
            return json.dumps(data).encode()

        def deserialize(data: bytes) -> dict:
            return json.loads(data)

        super().__init__(
            config=config,
            serializer=serialize,
            deserializer=deserialize,
            content_type="application/json",
        )

        # Override timestamp endpoint with Pydantic validation
        @self.app.post("/timestamp", response_model=TimestampResponse)
        async def timestamp(request: TimestampRequest) -> TimestampResponse:
            """Handle timestamp request with Pydantic validation."""
            response_timestamp = datetime.now().isoformat()
            return TimestampResponse(
                request_timestamp=request.request_timestamp,
                response_timestamp=response_timestamp,
            )

    def _get_health_response(self) -> dict:
        """Customize health check response for REST."""
        return {
            "service": "REST API Responder",
            "status": "running",
            "format": "JSON over HTTP",
            "message": "Ready to process REST requests",
        }


# Create responder instance and expose app
responder = RestResponder()
app = responder.app
