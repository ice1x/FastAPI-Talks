"""
AVRO Responder Service

This service responds to Avro-serialized timestamp requests.
It deserializes incoming Avro messages, adds a response timestamp,
and returns the result in Avro format.
"""

import io
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for common imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import avro.io
import avro.schema
from fastapi import FastAPI, Request, Response

from common import TIMESTAMP_SCHEMA_AVRO

# Avro schema for timestamp messages
TIMESTAMP_SCHEMA = avro.schema.parse(TIMESTAMP_SCHEMA_AVRO)

app = FastAPI(
    title="AVRO Responder Service",
    description="Benchmark responder for Avro serialization",
    version="1.0.0",
)


@app.post("/timestamp")
async def handle_timestamp(request: Request):
    """
    Handle Avro-serialized timestamp requests.

    Deserializes the incoming Avro request, adds a response timestamp,
    and returns an Avro-serialized response.

    Args:
        request: FastAPI request containing Avro-serialized data

    Returns:
        Response with Avro-serialized timestamp data
    """
    # Read request body
    body = await request.body()

    # Deserialize Avro request
    reader = avro.io.DatumReader(TIMESTAMP_SCHEMA)
    bytes_reader = io.BytesIO(body)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    data = reader.read(decoder)

    # Add response timestamp
    data["response_timestamp"] = datetime.now().isoformat()

    # Serialize response
    writer = avro.io.DatumWriter(TIMESTAMP_SCHEMA)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer.write(data, encoder)

    return Response(content=bytes_writer.getvalue(), media_type="application/avro")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "AVRO Responder",
        "status": "running",
        "format": "Apache Avro Binary",
        "message": "Ready to process Avro requests",
    }
