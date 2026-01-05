"""
CBOR Requester Service

This service benchmarks CBOR (Concise Binary Object Representation) format.
It sends 1,000 HTTP requests with CBOR-encoded payloads and measures
response times for performance analysis.
"""

import asyncio
from datetime import datetime

import cbor2
import httpx
from fastapi import FastAPI

# Configuration
CBOR_RESPONDER_URL = "http://localhost:8000/timestamp"
REQUEST_COUNT = 1000
TIMEOUT = 30


app = FastAPI(
    title="CBOR Requester Service",
    description="Benchmark client for CBOR serialization",
    version="1.0.0",
)


async def send_cbor_request(client: httpx.AsyncClient, request_ts: str) -> dict:
    """
    Send a single CBOR-encoded request.

    Args:
        client: HTTP client for connection pooling
        request_ts: Request timestamp to send

    Returns:
        Dictionary with request and response timestamps
    """
    # Encode request with CBOR
    payload = cbor2.dumps({"request_timestamp": request_ts, "response_timestamp": ""})

    # Send request
    response = await client.post(
        CBOR_RESPONDER_URL,
        content=payload,
        headers={"Content-Type": "application/cbor"},
        timeout=TIMEOUT,
    )

    # Decode response
    result = cbor2.loads(response.content)
    return result


@app.get("/run-benchmark")
async def run_benchmark():
    """
    Execute CBOR serialization benchmark.

    Sends 1,000 requests with CBOR-encoded timestamps and collects
    response times for performance analysis.

    Returns:
        List of timestamp pairs (request/response)
    """
    results = []

    async with httpx.AsyncClient() as client:
        for i in range(REQUEST_COUNT):
            request_ts = datetime.now().isoformat()
            result = await send_cbor_request(client, request_ts)
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
        "service": "CBOR Requester",
        "status": "running",
        "format": "CBOR (Concise Binary Object Representation)",
        "endpoint": "/run-benchmark",
    }
