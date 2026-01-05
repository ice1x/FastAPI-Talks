"""
Benchmark Comparison Script

This script compares the performance of different communication protocols
(gRPC, Socket.IO, GraphQL) by analyzing response time data collected
from benchmark runs.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def read_metrics(file: Path) -> dict:
    """
    Read metrics from a JSON file.

    Args:
        file: Path to the JSON file containing benchmark metrics

    Returns:
        Dictionary containing the parsed metrics
    """
    if not file.exists():
        print(f"Warning: {file} not found. Skipping this benchmark.")
        return None
    return json.loads(file.read_bytes())


def process_grpc_data(grpc_data: list) -> pd.DataFrame:
    """
    Process gRPC benchmark data into a pandas DataFrame.

    Args:
        grpc_data: List of gRPC benchmark results

    Returns:
        DataFrame with request_id and response_time columns
    """
    df = pd.DataFrame(grpc_data)
    df["grpc_requester_timestamp"] = pd.to_datetime(df["grpc_requester_timestamp"])
    df["grpc_responder_timestamp"] = pd.to_datetime(df["grpc_responder_timestamp"])
    df["response_time"] = (
        df["grpc_responder_timestamp"] - df["grpc_requester_timestamp"]
    ).dt.total_seconds()
    return df[["request_id", "response_time"]]


def process_socketio_data(socketio_data: dict) -> pd.DataFrame:
    """
    Process Socket.IO benchmark data into a pandas DataFrame.

    Args:
        socketio_data: Dictionary containing Socket.IO benchmark results

    Returns:
        DataFrame with request_id and response_time columns
    """
    request_ts = pd.to_datetime(socketio_data["request_ts"])
    response_times = [
        (pd.to_datetime(ts) - request_ts).total_seconds()
        for ts in socketio_data["respond_ts"]
    ]

    return pd.DataFrame({
        "request_id": range(len(response_times)),
        "response_time": response_times
    })


def process_graphql_data(graphql_data: list) -> pd.DataFrame:
    """
    Process GraphQL benchmark data into a pandas DataFrame.

    Args:
        graphql_data: List of GraphQL benchmark results

    Returns:
        DataFrame with request_id and response_time columns
    """
    response_times = []
    for item in graphql_data:
        request_ts = pd.to_datetime(item["requestTimestamp"])
        response_ts = pd.to_datetime(item["responseTimestamp"])
        response_time = (response_ts - request_ts).total_seconds()
        response_times.append(response_time)

    return pd.DataFrame({
        "request_id": range(len(response_times)),
        "response_time": response_times
    })


def print_statistics(datasets: dict):
    """
    Print statistical summary for all datasets.

    Args:
        datasets: Dictionary mapping protocol names to DataFrames
    """
    print("\n" + "=" * 70)
    print("BENCHMARK STATISTICS")
    print("=" * 70)

    for name, df in datasets.items():
        if df is not None:
            print(f"\n{name}:")
            print(f"  Mean:     {df['response_time'].mean():.6f} seconds")
            print(f"  Median:   {df['response_time'].median():.6f} seconds")
            print(f"  Std Dev:  {df['response_time'].std():.6f} seconds")
            print(f"  Min:      {df['response_time'].min():.6f} seconds")
            print(f"  Max:      {df['response_time'].max():.6f} seconds")
            print(f"  Samples:  {len(df)}")

    print("\n" + "=" * 70)


def plot_comparison(datasets: dict):
    """
    Create comparison plots for all available datasets.

    Args:
        datasets: Dictionary mapping protocol names to DataFrames
    """
    # Filter out None values
    datasets = {k: v for k, v in datasets.items() if v is not None}

    if not datasets:
        print("No data available for plotting.")
        return

    plt.figure(figsize=(14, 8))

    # Define colors for consistency
    colors = {
        "gRPC": "blue",
        "Socket.IO": "green",
        "GraphQL": "red"
    }
    markers = {
        "gRPC": "o",
        "Socket.IO": "x",
        "GraphQL": "^"
    }

    # Plot response times for each protocol
    for name, df in datasets.items():
        plt.plot(
            df["request_id"],
            df["response_time"],
            marker=markers.get(name, "s"),
            label=f"{name} Response Time",
            alpha=0.6,
            markersize=3
        )

        # Plot average line
        avg_time = df["response_time"].mean()
        plt.axhline(
            y=avg_time,
            color=colors.get(name, "gray"),
            linestyle="--",
            label=f"{name} Avg: {avg_time:.6f}s",
            alpha=0.8
        )

    # Customize the chart
    plt.title("Communication Protocol Benchmark: Response Time Comparison", fontsize=16)
    plt.xlabel("Request ID", fontsize=12)
    plt.ylabel("Response Time (seconds)", fontsize=12)
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Save and show the plot
    plt.savefig("benchmark_comparison.png", dpi=300)
    print("\nPlot saved as 'benchmark_comparison.png'")
    plt.show()


def main():
    """Main execution function."""
    print("Loading benchmark data...")

    # Read all available benchmark files
    grpc_data = read_metrics(Path("grpc_out.txt"))
    socketio_data = read_metrics(Path("sio_out.txt"))
    graphql_data = read_metrics(Path("graphql_out.txt"))

    # Process data into DataFrames
    datasets = {}

    if grpc_data:
        datasets["gRPC"] = process_grpc_data(grpc_data)
        print("✓ gRPC data loaded")

    if socketio_data:
        datasets["Socket.IO"] = process_socketio_data(socketio_data)
        print("✓ Socket.IO data loaded")

    if graphql_data:
        datasets["GraphQL"] = process_graphql_data(graphql_data)
        print("✓ GraphQL data loaded")

    if not datasets:
        print("Error: No benchmark data found. Please run benchmarks first.")
        return

    # Print statistical analysis
    print_statistics(datasets)

    # Create comparison plot
    plot_comparison(datasets)


if __name__ == "__main__":
    main()
