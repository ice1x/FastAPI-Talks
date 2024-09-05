# import httpx
# from fastapi import FastAPI
# from datetime import datetime
# import asyncio
#
# # Initialize the FastAPI app
# app = FastAPI()
#
# # Define the GraphQL query template
# graphql_query = """
# query getTimestamps($requestTimestamp: DateTime!) {
#   getTimestamps(requestTimestamp: $requestTimestamp) {
#     requestTimestamp
#     responseTimestamp
#   }
# }
# """
#
# # The URL of the first service GraphQL endpoint
# GRAPHQL_ENDPOINT = "http://localhost:8080/graphql"
#
#
# # Function to make a single GraphQL request to the first service
# async def fetch_timestamps(session, request_timestamp):
#     # Define the request payload
#     payload = {
#         "query": graphql_query,
#         "variables": {
#             "requestTimestamp": request_timestamp.isoformat()
#         }
#     }
#
#     # Send the request to the first service
#     response = await session.post(GRAPHQL_ENDPOINT, json=payload)
#
#     # Parse the JSON response and extract the timestamps
#     data = response.json()
#     timestamps = data["data"]["getTimestamps"]
#     return timestamps
#
#
# # The GET method to make 1000 requests and aggregate the results
# @app.get("/aggregate-timestamps")
# async def aggregate_timestamps():
#     request_timestamp = datetime.utcnow()
#     num_requests = 1000
#     timestamps_list = []
#
#     # Use a single httpx.AsyncClient session for all requests
#     async with httpx.AsyncClient() as client:
#         # Create a list of tasks for 1000 GraphQL requests
#         tasks = [fetch_timestamps(client, request_timestamp) for _ in range(num_requests)]
#
#         # Run the tasks concurrently and gather the results
#         results = await asyncio.gather(*tasks)
#
#     # Collect the timestamps
#     for result in results:
#         timestamps_list.append(result)
#
#     # Return the aggregated list of timestamps
#     return timestamps_list


import httpx
from fastapi import FastAPI
from datetime import datetime
import asyncio

# Initialize the FastAPI app
app = FastAPI()

# Define the GraphQL query template
graphql_query = """
query getTimestamps($requestTimestamp: DateTime!) {
  getTimestamps(requestTimestamp: $requestTimestamp) {
    requestTimestamp
    responseTimestamp
  }
}
"""

# The URL of the first service GraphQL endpoint
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"


# Function to make a single GraphQL request to the first service
async def fetch_timestamps(session, request_timestamp):
    # Define the request payload
    payload = {
        "query": graphql_query,
        "variables": {
            "requestTimestamp": request_timestamp.isoformat()
        }
    }

    # Send the request to the first service
    response = await session.post(GRAPHQL_ENDPOINT, json=payload, timeout=10.0)

    # Parse the JSON response and extract the timestamps
    data = response.json()
    timestamps = data["data"]["getTimestamps"]
    return timestamps


# The GET method to make 1000 requests and aggregate the results
@app.get("/aggregate-timestamps")
async def aggregate_timestamps():
    num_requests = 1000
    timestamps_list = []

    # Set connection limits and timeouts
    limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)

    # Use a single httpx.AsyncClient session for all requests with increased pool limits
    async with httpx.AsyncClient(limits=limits) as client:
        # Batch the requests in smaller groups to avoid overwhelming the pool
        batch_size = 50
        for i in range(0, num_requests, batch_size):
            request_timestamp = datetime.utcnow()
            tasks = [fetch_timestamps(client, request_timestamp) for _ in range(batch_size)]

            # Run the tasks concurrently and gather the results
            results = await asyncio.gather(*tasks)
            timestamps_list.extend(results)

    # Return the aggregated list of timestamps
    return timestamps_list

