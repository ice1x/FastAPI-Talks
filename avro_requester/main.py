"""
AVRO Requester Service

This service benchmarks Apache Avro binary serialization format.
It sends 1,000 HTTP requests with Avro-serialized payloads and measures
response times for performance analysis.
"""

import asyncio
import io
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for common imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import avro.schema
import httpx
from avro.datafile import DataFileWriter
from avro.io import BinaryDecoder, DatumReader, DatumWriter
from fastapi import FastAPI

from common import TIMESTAMP_SCHEMA_AVRO

# Avro schema for timestamp messages
TIMESTAMP_SCHEMA = avro.schema.parse(TIMESTAMP_SCHEMA_AVRO)

# Configuration
AVRO_RESPONDER_URL = "http://localhost:8000/timestamp"
REQUEST_COUNT = 1000
TIMEOUT = 30


app = FastAPI(
    title="AVRO Requester Service",
    description="Benchmark client for Avro serialization",
    version="1.0.0",
)


async def send_avro_request(client: httpx.AsyncClient, request_ts: str) -> dict:
    """
    Send a single Avro-serialized request.

    Args:
        client: HTTP client for connection pooling
        request_ts: Request timestamp to send

    Returns:
        Dictionary with request and response timestamps
    """
    # Serialize request with Avro
    writer = avro.io.DatumWriter(TIMESTAMP_SCHEMA)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer.write({"request_timestamp": request_ts, "response_timestamp": ""}, encoder)

    # Send request
    response = await client.post(
        AVRO_RESPONDER_URL,
        content=bytes_writer.getvalue(),
        headers={"Content-Type": "application/avro"},
        timeout=TIMEOUT,
    )

    # Deserialize response
    reader = avro.io.DatumReader(TIMESTAMP_SCHEMA)
    bytes_reader = io.BytesIO(response.content)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    result = reader.read(decoder)

    return result


@app.get("/run-benchmark")
async def run_benchmark():
    """
    Execute Avro serialization benchmark.

    Sends 1,000 requests with Avro-serialized timestamps and collects
    response times for performance analysis.

    Returns:
        List of timestamp pairs (request/response)
    """
    results = []

    async with httpx.AsyncClient() as client:
        for i in range(REQUEST_COUNT):
            request_ts = datetime.now().isoformat()
            result = await send_avro_request(client, request_ts)
            results.append(
                {
                    "request_id": i,
                    "request_timestamp": result["request_timestamp"],
                    "response_timestamp": result["response_timestamp"],
                }
            )

    return results


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "AVRO Requester",
        "status": "running",
        "format": "Apache Avro Binary",
        "endpoint": "/run-benchmark",
    }
