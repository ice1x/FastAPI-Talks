#!/usr/bin/env python3
"""
Automated Benchmark Runner

This script automates the execution of all communication protocol benchmarks.
It starts the responder and requester services, executes the benchmarks,
and collects the results.
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import httpx


class BenchmarkRunner:
    """
    Manages the execution of protocol benchmarks.
    """

    def __init__(self):
        self.processes = []

    def start_service(
        self, name: str, directory: str, command: list, port: int, wait_time: int = 3
    ) -> subprocess.Popen:
        """
        Start a service process.

        Args:
            name: Service name for logging
            directory: Working directory for the service
            command: Command to execute
            port: Port the service will listen on
            wait_time: Seconds to wait for service startup

        Returns:
            The subprocess.Popen object
        """
        print(f"Starting {name}...")
        process = subprocess.Popen(
            command, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        self.processes.append(process)
        time.sleep(wait_time)

        # Verify service is running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"Error: {name} failed to start")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None

        print(f"✓ {name} started on port {port}")
        return process

    async def execute_benchmark(self, name: str, url: str, output_file: str) -> bool:
        """
        Execute a benchmark by sending HTTP request.

        Args:
            name: Benchmark name for logging
            url: URL to send request to
            output_file: File to save results

        Returns:
            True if successful, False otherwise
        """
        print(f"\nExecuting {name} benchmark...")
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.get(url)
                response.raise_for_status()

                # Save results
                with open(output_file, "w") as f:
                    if isinstance(response.json(), list):
                        json.dump(response.json(), f)
                    else:
                        json.dump(response.json(), f)

                print(f"✓ {name} benchmark completed")
                print(f"  Results saved to {output_file}")
                return True

        except Exception as e:
            print(f"✗ {name} benchmark failed: {e}")
            return False

    def stop_all_services(self):
        """Stop all running service processes."""
        print("\nStopping all services...")
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except (subprocess.TimeoutExpired, Exception):
                process.kill()
        print("✓ All services stopped")

    async def run_grpc_benchmark(self) -> bool:
        """Run gRPC benchmark."""
        print("\n" + "=" * 60)
        print("gRPC BENCHMARK")
        print("=" * 60)

        # Start responder
        responder = self.start_service(
            "gRPC Responder", "grpc_responder", [sys.executable, "main.py"], 50051
        )
        if not responder:
            return False

        # Start requester
        requester = self.start_service(
            "gRPC Requester",
            "grpc_requester",
            ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
            8000,
        )
        if not requester:
            return False

        # Execute benchmark
        success = await self.execute_benchmark(
            "gRPC", "http://127.0.0.1:8000/api/run", "grpc_out.txt"
        )

        # Stop services
        requester.terminate()
        responder.terminate()
        time.sleep(2)

        return success

    async def run_socketio_benchmark(self) -> bool:
        """Run Socket.IO benchmark."""
        print("\n" + "=" * 60)
        print("SOCKET.IO BENCHMARK")
        print("=" * 60)

        # Start responder
        responder = self.start_service(
            "Socket.IO Responder",
            "sio_responder",
            ["uvicorn", "main:sio_app", "--host", "0.0.0.0", "--port", "8000"],
            8000,
        )
        if not responder:
            return False

        # Start requester
        requester = self.start_service(
            "Socket.IO Requester",
            "sio_requester",
            ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"],
            8080,
            wait_time=5,  # Extra time for Socket.IO connection
        )
        if not requester:
            return False

        # Execute benchmark
        success = await self.execute_benchmark(
            "Socket.IO", "http://127.0.0.1:8080/send-timestamp", "sio_out.txt"
        )

        # Stop services
        requester.terminate()
        responder.terminate()
        time.sleep(2)

        return success

    async def run_graphql_benchmark(self) -> bool:
        """Run GraphQL benchmark."""
        print("\n" + "=" * 60)
        print("GRAPHQL BENCHMARK")
        print("=" * 60)

        # Start responder
        responder = self.start_service(
            "GraphQL Responder",
            "graphql_responder",
            ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
            8000,
        )
        if not responder:
            return False

        # Start requester
        requester = self.start_service(
            "GraphQL Requester",
            "graphql_requester",
            ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"],
            8080,
        )
        if not requester:
            return False

        # Execute benchmark
        success = await self.execute_benchmark(
            "GraphQL", "http://127.0.0.1:8080/aggregate-timestamps", "graphql_out.txt"
        )

        # Stop services
        requester.terminate()
        responder.terminate()
        time.sleep(2)

        return success

    async def run_all_benchmarks(self):
        """Run all benchmarks sequentially."""
        print("\n" + "=" * 60)
        print("FASTAPI COMMUNICATION PROTOCOLS BENCHMARK")
        print("=" * 60)
        print("\nThis will run benchmarks for:")
        print("  - gRPC")
        print("  - Socket.IO")
        print("  - GraphQL")
        print("\nEach benchmark sends 1,000 requests and measures response time.")
        print("=" * 60)

        results = {"gRPC": False, "Socket.IO": False, "GraphQL": False}

        try:
            results["gRPC"] = await self.run_grpc_benchmark()
            results["Socket.IO"] = await self.run_socketio_benchmark()
            results["GraphQL"] = await self.run_graphql_benchmark()

        except KeyboardInterrupt:
            print("\n\nBenchmark interrupted by user")
        finally:
            self.stop_all_services()

        # Print summary
        print("\n" + "=" * 60)
        print("BENCHMARK SUMMARY")
        print("=" * 60)
        for protocol, success in results.items():
            status = "✓ Completed" if success else "✗ Failed"
            print(f"{protocol:15} {status}")
        print("=" * 60)

        # Run comparison if all succeeded
        if all(results.values()):
            print("\nRunning comparison analysis...")
            subprocess.run([sys.executable, "compare.py"])
        else:
            print("\nSome benchmarks failed. Skipping comparison.")


async def main():
    """Main entry point."""
    runner = BenchmarkRunner()
    await runner.run_all_benchmarks()


if __name__ == "__main__":
    asyncio.run(main())
