"""
GraphQL Requester Service

This service acts as a benchmark client for the GraphQL responder.
It sends 1,000 GraphQL queries in batches and collects response timestamps
for performance analysis.
"""

import asyncio
from datetime import datetime

import httpx
from fastapi import FastAPI

# Initialize the FastAPI app
app = FastAPI(
    title="GraphQL Requester Service",
    description="Benchmark client for GraphQL timestamp queries",
    version="1.0.0"
)

# GraphQL query template for fetching timestamps
GRAPHQL_QUERY = """
query getTimestamps($requestTimestamp: DateTime!) {
  getTimestamps(requestTimestamp: $requestTimestamp) {
    requestTimestamp
    responseTimestamp
  }
}
"""

# GraphQL endpoint URL (configurable via environment variable)
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"


async def fetch_timestamps(session: httpx.AsyncClient, request_timestamp: datetime) -> dict:
    """
    Send a single GraphQL query request and return the response.

    Args:
        session: HTTP client session for connection pooling
        request_timestamp: The timestamp to send in the query

    Returns:
        Dictionary containing request and response timestamps
    """
    payload = {
        "query": GRAPHQL_QUERY,
        "variables": {
            "requestTimestamp": request_timestamp.isoformat()
        }
    }

    response = await session.post(
        GRAPHQL_ENDPOINT,
        json=payload,
        timeout=10.0
    )

    data = response.json()
    return data["data"]["getTimestamps"]


@app.get("/aggregate-timestamps")
async def aggregate_timestamps():
    """
    Execute 1,000 GraphQL queries in batches and aggregate results.

    This endpoint sends GraphQL timestamp queries in batches of 50
    to avoid overwhelming the connection pool. Results are collected
    and returned for benchmark analysis.

    Returns:
        List of timestamp pairs (request/response) from all queries
    """
    num_requests = 1000
    batch_size = 50
    timestamps_list = []

    # Configure connection pooling for optimal performance
    limits = httpx.Limits(
        max_connections=100,
        max_keepalive_connections=20
    )

    async with httpx.AsyncClient(limits=limits) as client:
        # Process requests in batches
        for i in range(0, num_requests, batch_size):
            request_timestamp = datetime.utcnow()

            # Create batch of concurrent requests
            tasks = [
                fetch_timestamps(client, request_timestamp)
                for _ in range(batch_size)
            ]

            # Execute batch concurrently
            results = await asyncio.gather(*tasks)
            timestamps_list.extend(results)

    return timestamps_list


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "GraphQL Requester",
        "status": "running",
        "endpoint": "/aggregate-timestamps"
    }
