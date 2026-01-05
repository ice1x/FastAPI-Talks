"""
Socket.IO Responder Service

This service provides a Socket.IO endpoint that responds to timestamp requests.
It receives a timestamp request and sends back 1,000 response timestamps
for benchmark analysis.
"""

from datetime import datetime

import socketio
from fastapi import FastAPI

# Create a Socket.IO server with ASGI support
sio = socketio.AsyncServer(async_mode="asgi")

# Create a FastAPI application
app = FastAPI(
    title="Socket.IO Responder Service",
    description="Benchmark responder for Socket.IO timestamp queries",
    version="1.0.0",
)

# Integrate Socket.IO server with FastAPI
sio_app = socketio.ASGIApp(sio, app)


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "service": "Socket.IO Responder",
        "status": "running",
        "message": "Socket.IO server is running and ready to accept connections",
    }


@sio.event
async def connect(sid, environ):
    """
    Handle client connection events.

    Args:
        sid: Session ID of the connected client
        environ: WSGI environment dictionary
    """
    print(f"✓ Client {sid} connected")


@sio.event
async def disconnect(sid):
    """
    Handle client disconnection events.

    Args:
        sid: Session ID of the disconnected client
    """
    print(f"✓ Client {sid} disconnected")


@sio.event
async def timestamp(sid, data):
    """
    Handle timestamp request events.

    Receives a timestamp request and sends back 1,000 response timestamps
    to the requesting client.

    Args:
        sid: Session ID of the requesting client
        data: Dictionary containing the request timestamp
    """
    request_ts = data.get("request_ts")
    print(f"Received timestamp request from {sid}: {request_ts}")

    # Send 1,000 timestamp responses
    for i in range(1000):
        respond_ts = datetime.now().isoformat()
        await sio.emit(
            "timestamp_response", {"request_ts": request_ts, "respond_ts": respond_ts}, room=sid
        )

    print(f"✓ Sent 1,000 responses to client {sid}")


# Run the application with Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(sio_app, host="0.0.0.0", port=8000)
