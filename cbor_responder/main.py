"""
CBOR Responder Service

This service responds to CBOR-encoded timestamp requests.
It decodes incoming CBOR messages, adds a response timestamp,
and returns the result in CBOR format.
"""

from datetime import datetime

import cbor2
from fastapi import FastAPI, Request, Response

app = FastAPI(
    title="CBOR Responder Service",
    description="Benchmark responder for CBOR serialization",
    version="1.0.0",
)


@app.post("/timestamp")
async def handle_timestamp(request: Request):
    """
    Handle CBOR-encoded timestamp requests.

    Decodes the incoming CBOR request, adds a response timestamp,
    and returns a CBOR-encoded response.

    Args:
        request: FastAPI request containing CBOR-encoded data

    Returns:
        Response with CBOR-encoded timestamp data
    """
    # Read and decode request body
    body = await request.body()
    data = cbor2.loads(body)

    # Add response timestamp
    data["response_timestamp"] = datetime.now().isoformat()

    # Encode and return response
    return Response(content=cbor2.dumps(data), media_type="application/cbor")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "CBOR Responder",
        "status": "running",
        "format": "CBOR (Concise Binary Object Representation)",
        "message": "Ready to process CBOR requests",
    }
