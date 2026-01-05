"""
REST API Responder Service

This service provides a standard REST API endpoint that responds to JSON requests.
It receives a timestamp in JSON format and returns it along with the server's
current timestamp.
"""

from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel


class TimestampRequest(BaseModel):
    """Request model for timestamp endpoint."""
    request_timestamp: str


class TimestampResponse(BaseModel):
    """Response model for timestamp endpoint."""
    request_timestamp: str
    response_timestamp: str


app = FastAPI(
    title="REST API Responder Service",
    description="Benchmark responder for REST API with JSON",
    version="1.0.0"
)


@app.post("/timestamp", response_model=TimestampResponse)
async def handle_timestamp(request: TimestampRequest) -> TimestampResponse:
    """
    Handle REST API timestamp requests.

    Receives a JSON request with a timestamp and returns it along with
    the current server timestamp.

    Args:
        request: TimestampRequest containing the request timestamp

    Returns:
        TimestampResponse with both request and response timestamps
    """
    return TimestampResponse(
        request_timestamp=request.request_timestamp,
        response_timestamp=datetime.now().isoformat()
    )


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "REST API Responder",
        "status": "running",
        "format": "JSON over HTTP",
        "message": "Ready to process REST requests"
    }
