from fastapi import FastAPI

# from grpc import StatusCode
# from grpc_interceptor.exceptions import NotFound, GrpcException
from datetime import UTC, datetime

from pb.hello_grpc_pb2 import Response
from pb.hello_grpc_pb2_grpc import GRPCServiceServicer
from google.protobuf.timestamp_pb2 import Timestamp

app = FastAPI()


# # A simple HTML page for testing the WebSocket connection
# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>WebSocket Test</title>
#     </head>
#     <body>
#         <h1>WebSocket Test</h1>
#         <button onclick="connectWebSocket()">Connect WebSocket</button>
#         <p id="messages"></p>
#         <script>
#             let socket;
#             function connectWebSocket() {
#                 socket = new WebSocket("ws://localhost:8000/ws");
#                 socket.onmessage = function(event) {
#                     document.getElementById("messages").innerHTML += `<p>${event.data}</p>`;
#                 };
#                 socket.onopen = function(event) {
#                     socket.send("Hello from the client!");
#                 };
#             }
#         </script>
#     </body>
# </html>
# """
#
#
# @app.get("/")
# async def get():
#     return HTMLResponse(html)
#
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_text(f"Message text was: {data}")
#     except WebSocketDisconnect:
#         print("Client disconnected")
#
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


class BaseServicer(GRPCServiceServicer):

    def GetTimestamp(self, request, context):
        now = datetime.now(UTC)
        timestamp = Timestamp()
        timestamp.FromDatetime(now)

        return Response(response_ts=timestamp)
