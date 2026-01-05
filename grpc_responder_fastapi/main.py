import asyncio
from concurrent import futures

import uvicorn
from api.grpc.grpc_endpoint import BaseServicer
from fastapi import FastAPI
from grpc import aio

# from your_grpc_module import YourServicer, add_YourServicer_to_server  # Import your gRPC definitions
from pb.hello_grpc_pb2_grpc import add_GRPCServiceServicer_to_server

app = FastAPI()


class ResponseTimestampService(BaseServicer):
    pass


# Define FastAPI endpoints
@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI"}


# Define a function to serve the gRPC server
async def serve_grpc():
    server = aio.server()
    add_GRPCServiceServicer_to_server(ResponseTimestampService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


# Define a function to run FastAPI
async def serve_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


# Use asyncio to run both servers concurrently
async def main():
    await asyncio.gather(
        serve_fastapi(),
        serve_grpc(),
    )


if __name__ == "__main__":
    asyncio.run(main())
