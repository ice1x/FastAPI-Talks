"""
GraphQL Responder Service

This service provides a GraphQL endpoint that responds to timestamp queries.
It receives a request timestamp and returns it along with the current server timestamp.
"""

from datetime import datetime

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Timestamps:
    """
    GraphQL type representing request and response timestamps.

    Attributes:
        request_timestamp: The timestamp from the client request
        response_timestamp: The timestamp when the server processed the request
    """
    request_timestamp: datetime
    response_timestamp: datetime


@strawberry.type
class Query:
    """
    GraphQL query root defining available queries.
    """

    @strawberry.field
    def get_timestamps(self, request_timestamp: datetime) -> Timestamps:
        """
        Query to get request and response timestamps.

        Args:
            request_timestamp: The timestamp from the client

        Returns:
            Timestamps object containing both request and response timestamps
        """
        response_timestamp = datetime.utcnow()
        return Timestamps(
            request_timestamp=request_timestamp,
            response_timestamp=response_timestamp
        )


# Create the GraphQL schema
schema = strawberry.Schema(Query)

# Initialize the FastAPI app
app = FastAPI(
    title="GraphQL Responder Service",
    description="Benchmark responder for GraphQL timestamp queries",
    version="1.0.0"
)

# Add the GraphQL router
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "GraphQL Responder",
        "status": "running",
        "endpoint": "/graphql"
    }
