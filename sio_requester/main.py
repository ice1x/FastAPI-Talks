import asyncio
import socketio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from datetime import datetime

# Create a Socket.IO client
sio = socketio.AsyncClient()

# This will store the list of timestamps received
timestamp_list = []

# This event is used to signal that all responses have been received
timestamps_received_event = asyncio.Event()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        # Connect to the Socket.IO server, specify namespace if necessary
        await sio.connect("http://127.0.0.1:8000")  # Default namespace
        print("Connected to the server")
        yield
    except Exception as e:
        print(f"Failed to connect: {e}")
    finally:
        # Disconnect from the server if connected
        if sio.connected:
            await sio.disconnect()
            print("Disconnected from the server")

# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/send-timestamp")
async def send_timestamp():
    global timestamp_list
    global timestamps_received_event

    # Clear the list for a new request
    timestamp_list = []
    timestamps_received_event.clear()

    # Get the current timestamp
    request_ts = datetime.now().isoformat()

    try:
        # Send the request timestamp to the Socket.IO server
        await sio.emit("timestamp", {"request_ts": request_ts})

        # Wait for the list to be populated by timestamp_response handler
        await asyncio.wait_for(timestamps_received_event.wait(), timeout=10)  # Adjust timeout as needed

        return {"status": "timestamps received", "request_ts": request_ts, "respond_ts": timestamp_list}

    except asyncio.TimeoutError:
        return {"status": "timeout", "request_ts": request_ts, "respond_ts": timestamp_list}

    except Exception as e:
        return {"error": str(e)}

@sio.event
async def timestamp_response(data):
    global timestamp_list
    global timestamps_received_event

    # Append the received timestamp to the list
    timestamp_list.append(data["respond_ts"])

    # If 1,000 responses have been received, set the event
    if len(timestamp_list) >= 1000:
        timestamps_received_event.set()
