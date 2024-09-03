import json
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def read_metrics(file):
    return json.loads(Path(file).read_bytes())


grpc_data = read_metrics(Path("grpc_out.txt"))
socketio_data = read_metrics(Path("sio_out.txt"))


# Step 1: Convert gRPC dataset to pandas DataFrame
df_grpc = pd.DataFrame(grpc_data)
df_grpc["grpc_requester_timestamp"] = pd.to_datetime(df_grpc["grpc_requester_timestamp"])
df_grpc["grpc_responder_timestamp"] = pd.to_datetime(df_grpc["grpc_responder_timestamp"])
df_grpc["response_time"] = (df_grpc["grpc_responder_timestamp"] - df_grpc["grpc_requester_timestamp"]).dt.total_seconds()

# Step 2: Process the Socket.IO dataset
request_ts_socketio = pd.to_datetime(socketio_data["request_ts"])
response_times_socketio = [(pd.to_datetime(ts) - request_ts_socketio).total_seconds() for ts in socketio_data["respond_ts"]]

# Step 3: Create a DataFrame for the Socket.IO dataset
df_socketio = pd.DataFrame({
    "request_id": range(len(response_times_socketio)),
    "response_time": response_times_socketio
})

# Step 4: Calculate the average response time for both datasets
average_response_time_grpc = df_grpc["response_time"].mean()
average_response_time_socketio = df_socketio["response_time"].mean()

# Step 5: Plotting both datasets
plt.figure(figsize=(12, 8))

# Plot the gRPC dataset
plt.plot(df_grpc["request_id"], df_grpc["response_time"], marker="o", label="gRPC Response Time")

# Plot the Socket.IO dataset
plt.plot(df_socketio["request_id"], df_socketio["response_time"], marker="x", label="Socket.IO Response Time")

# Plot average response times
plt.axhline(y=average_response_time_grpc, color="r", linestyle="--", label=f"gRPC Avg Response Time: {average_response_time_grpc:.6f}s")
plt.axhline(y=average_response_time_socketio, color="g", linestyle="--", label=f"Socket.IO Avg Response Time: {average_response_time_socketio:.6f}s")

# Customize the chart
plt.title("gRPC vs Socket.IO Response Time Comparison")
plt.xlabel("Request ID")
plt.ylabel("Response Time (seconds)")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
