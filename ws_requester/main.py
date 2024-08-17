import asyncio
import websockets
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


async def websocket_client():
    uri = "ws://localhost:8000/ws"  # Replace with the WebSocket server's URI
    async with websockets.connect(uri) as websocket:
        # Send a message to the WebSocket server
        await websocket.send("Hello from the client service!")

        # Wait for a message from the WebSocket server
        response = await websocket.recv()
        print(f"Received from server: {response}")

@app.get("/start-websocket-client")
async def start_websocket_client(background_tasks: BackgroundTasks):
    background_tasks.add_task(websocket_client)
    return {"message": "WebSocket client started in the background"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
