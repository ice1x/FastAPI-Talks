import socketio
from fastapi import FastAPI
from datetime import datetime

# Create a Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi")

# Create a FastAPI application
app = FastAPI()

# Integrate Socket.IO server with FastAPI
sio_app = socketio.ASGIApp(sio, app)


@app.get("/")
def read_root():
    return {"message": "Socket.IO server running!"}


@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")


@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")


@sio.event
async def timestamp(sid, data):
    print(f"Received timestamp data: {data}")
    request_ts = data.get("request_ts")

    # Simulate sending 1,000 responses
    for _ in range(1000):
        respond_ts = datetime.now().isoformat()
        await sio.emit("timestamp_response", {"request_ts": request_ts, "respond_ts": respond_ts}, room=sid)

# Run the application with Uvicorn, using "sio_app" as the ASGI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(sio_app, host="0.0.0.0", port=8000)
