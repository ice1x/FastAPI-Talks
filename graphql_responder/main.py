from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
import strawberry
from datetime import datetime

# Define the GraphQL schema using Strawberry
@strawberry.type
class Timestamps:
    request_timestamp: datetime
    response_timestamp: datetime

# Define the GraphQL Query
@strawberry.type
class Query:
    @strawberry.field
    def get_timestamps(self, request_timestamp: datetime) -> Timestamps:
        response_timestamp = datetime.utcnow()
        return Timestamps(
            request_timestamp=request_timestamp,
            response_timestamp=response_timestamp
        )

# Create the GraphQL schema
schema = strawberry.Schema(Query)

# Initialize the FastAPI app
app = FastAPI()

# Add the GraphQL router
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Root endpoint for health check or simple information
@app.get("/")
async def root():
    return {"message": "This is the second FastAPI service with a GraphQL endpoint"}

