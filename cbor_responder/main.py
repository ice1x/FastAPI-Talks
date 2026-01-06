"""
CBOR Responder Service

This service responds to CBOR-encoded timestamp requests.
It decodes incoming CBOR messages, adds a response timestamp,
and returns the result in CBOR format.
"""

import sys
from pathlib import Path

# Add parent directory to path for common imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import cbor2

from common import BaseBenchmarkResponder, BenchmarkConfig


class CborResponder(BaseBenchmarkResponder):
    """CBOR benchmark responder using binary encoding."""

    def __init__(self):
        """Initialize CBOR responder with CBOR serializer/deserializer."""
        config = BenchmarkConfig(protocol_name="CBOR", responder_port=8000)

        # CBOR serializer/deserializer
        def serialize(data: dict) -> bytes:
            return cbor2.dumps(data)

        def deserialize(data: bytes) -> dict:
            return cbor2.loads(data)

        super().__init__(
            config=config,
            serializer=serialize,
            deserializer=deserialize,
            content_type="application/cbor",
        )

    def _get_health_response(self) -> dict:
        """Customize health check response for CBOR."""
        return {
            "service": "CBOR Responder",
            "status": "running",
            "format": "CBOR (Concise Binary Object Representation)",
            "message": "Ready to process CBOR requests",
        }


# Create responder instance and expose app
responder = CborResponder()
app = responder.app
