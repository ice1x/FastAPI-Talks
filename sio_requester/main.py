"""
Socket.IO Requester Service

This service acts as a benchmark client for the Socket.IO responder.
It connects to a Socket.IO server, sends a timestamp request, and collects
1,000 response timestamps for performance analysis.
"""

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime

import socketio
from fastapi import FastAPI

# Configuration - can be overridden via environment variables
SOCKETIO_SERVER_URL = "http://127.0.0.1:8000"
RESPONSE_TIMEOUT = 30  # seconds
EXPECTED_RESPONSES = 1000

# Create a Socket.IO client
sio = socketio.AsyncClient()

# Storage for received timestamps
timestamp_list = []

# Event to signal completion of all responses
timestamps_received_event = asyncio.Event()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage Socket.IO connection lifecycle.

    Connects to the Socket.IO server on startup and disconnects on shutdown.
    """
    try:
        # Connect to the Socket.IO server
        await sio.connect(SOCKETIO_SERVER_URL)
        print(f"✓ Connected to Socket.IO server at {SOCKETIO_SERVER_URL}")
        yield
    except Exception as e:
        print(f"✗ Failed to connect to Socket.IO server: {e}")
        raise
    finally:
        # Disconnect from the server if connected
        if sio.connected:
            await sio.disconnect()
            print("✓ Disconnected from Socket.IO server")


# Initialize FastAPI app with lifespan
app = FastAPI(
    lifespan=lifespan,
    title="Socket.IO Requester Service",
    description="Benchmark client for Socket.IO timestamp queries",
    version="1.0.0",
)


@app.get("/send-timestamp")
async def send_timestamp():
    """
    Execute Socket.IO timestamp benchmark.

    Sends a timestamp to the Socket.IO server and waits to receive
    1,000 response timestamps. Returns all collected timestamps for
    benchmark analysis.

    Returns:
        Dictionary containing:
        - status: Request status (success/timeout/error)
        - request_ts: Initial request timestamp
        - respond_ts: List of response timestamps
    """
    global timestamp_list
    global timestamps_received_event

    # Reset state for new benchmark run
    timestamp_list = []
    timestamps_received_event.clear()

    # Generate request timestamp
    request_ts = datetime.now().isoformat()

    try:
        # Send the timestamp request to the Socket.IO server
        await sio.emit("timestamp", {"request_ts": request_ts})

        # Wait for all responses to be received
        await asyncio.wait_for(timestamps_received_event.wait(), timeout=RESPONSE_TIMEOUT)

        return {
            "status": "timestamps received",
            "request_ts": request_ts,
            "respond_ts": timestamp_list,
        }

    except asyncio.TimeoutError:
        return {
            "status": "timeout",
            "request_ts": request_ts,
            "respond_ts": timestamp_list,
            "received_count": len(timestamp_list),
            "expected_count": EXPECTED_RESPONSES,
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "request_ts": request_ts,
            "respond_ts": timestamp_list,
        }


@sio.event
async def timestamp_response(data):
    """
    Handle timestamp response events from Socket.IO server.

    Args:
        data: Dictionary containing the response timestamp
    """
    global timestamp_list
    global timestamps_received_event

    # Append the received timestamp to the list
    timestamp_list.append(data["respond_ts"])

    # Check if all expected responses have been received
    if len(timestamp_list) >= EXPECTED_RESPONSES:
        timestamps_received_event.set()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "Socket.IO Requester",
        "status": "running" if sio.connected else "disconnected",
        "server": SOCKETIO_SERVER_URL,
        "endpoint": "/send-timestamp",
    }
