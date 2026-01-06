"""
AVRO Responder Service

This service responds to Avro-serialized timestamp requests.
It deserializes incoming Avro messages, adds a response timestamp,
and returns the result in Avro format.
"""

import io
import sys
from pathlib import Path

# Add parent directory to path for common imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import avro.io
import avro.schema

from common import BaseBenchmarkResponder, BenchmarkConfig, TIMESTAMP_SCHEMA_AVRO


class AvroResponder(BaseBenchmarkResponder):
    """AVRO benchmark responder using binary serialization."""

    def __init__(self):
        """Initialize AVRO responder with Avro serializer/deserializer."""
        config = BenchmarkConfig(protocol_name="AVRO", responder_port=8000)

        # Parse AVRO schema
        self.schema = avro.schema.parse(TIMESTAMP_SCHEMA_AVRO)

        # AVRO serializer/deserializer
        def serialize(data: dict) -> bytes:
            writer = avro.io.DatumWriter(self.schema)
            bytes_writer = io.BytesIO()
            encoder = avro.io.BinaryEncoder(bytes_writer)
            writer.write(data, encoder)
            return bytes_writer.getvalue()

        def deserialize(data: bytes) -> dict:
            reader = avro.io.DatumReader(self.schema)
            bytes_reader = io.BytesIO(data)
            decoder = avro.io.BinaryDecoder(bytes_reader)
            return reader.read(decoder)

        super().__init__(
            config=config,
            serializer=serialize,
            deserializer=deserialize,
            content_type="application/avro",
        )

    def _get_health_response(self) -> dict:
        """Customize health check response for AVRO."""
        return {
            "service": "AVRO Responder",
            "status": "running",
            "format": "Apache Avro Binary",
            "message": "Ready to process Avro requests",
        }


# Create responder instance and expose app
responder = AvroResponder()
app = responder.app
