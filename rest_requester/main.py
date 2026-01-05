"""
REST API Requester Service

This service benchmarks standard REST API communication with JSON serialization.
It sends 1,000 HTTP requests with JSON payloads and measures response times
for performance analysis.
"""

from datetime import datetime

import httpx
from fastapi import FastAPI

# Configuration
REST_RESPONDER_URL = "http://localhost:8000/timestamp"
REQUEST_COUNT = 1000
TIMEOUT = 30


app = FastAPI(
    title="REST API Requester Service",
    description="Benchmark client for REST API with JSON",
    version="1.0.0"
)


async def send_rest_request(client: httpx.AsyncClient, request_ts: str) -> dict:
    """
    Send a single REST API request with JSON payload.

    Args:
        client: HTTP client for connection pooling
        request_ts: Request timestamp to send

    Returns:
        Dictionary with request and response timestamps
    """
    payload = {
        "request_timestamp": request_ts
    }

    response = await client.post(
        REST_RESPONDER_URL,
        json=payload,
        timeout=TIMEOUT
    )

    return response.json()


@app.get("/run-benchmark")
async def run_benchmark():
    """
    Execute REST API benchmark.

    Sends 1,000 requests with JSON-encoded timestamps and collects
    response times for performance analysis.

    Returns:
        List of timestamp pairs (request/response)
    """
    results = []

    async with httpx.AsyncClient() as client:
        for i in range(REQUEST_COUNT):
            request_ts = datetime.now().isoformat()
            result = await send_rest_request(client, request_ts)
            results.append({
                "request_id": i,
                "request_timestamp": result["request_timestamp"],
                "response_timestamp": result["response_timestamp"]
            })

    return results


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "REST API Requester",
        "status": "running",
        "format": "JSON over HTTP",
        "endpoint": "/run-benchmark"
    }
