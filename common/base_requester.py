"""Base class for all benchmark requester services."""

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Protocol

import httpx
from fastapi import FastAPI

from .config import BenchmarkConfig


class Serializer(Protocol):
    """Protocol for serializer functions."""

    def __call__(self, data: Dict[str, Any]) -> Any:
        """Serialize data to protocol-specific format."""
        ...


class Deserializer(Protocol):
    """Protocol for deserializer functions."""

    def __call__(self, data: Any) -> Dict[str, Any]:
        """Deserialize protocol-specific format to dict."""
        ...


class BaseBenchmarkRequester:
    """
    Base class for all benchmark requester services.

    This class provides common functionality for benchmark requesters:
    - FastAPI app creation with metadata
    - Health check endpoint
    - Generic benchmark execution loop
    - Result collection and formatting

    Subclasses must implement:
    - _send_request(): Protocol-specific request logic
    """

    def __init__(
        self,
        config: BenchmarkConfig,
        serializer: Optional[Serializer] = None,
        deserializer: Optional[Deserializer] = None,
    ):
        """
        Initialize base requester.

        Args:
            config: Benchmark configuration
            serializer: Function to serialize request data (optional)
            deserializer: Function to deserialize response data (optional)
        """
        self.config = config
        self.serializer = serializer
        self.deserializer = deserializer
        self.app = self._create_app()
        self._configure_routes()

    def _create_app(self) -> FastAPI:
        """Create FastAPI application with metadata."""
        return FastAPI(
            title=f"{self.config.protocol_name} Requester Service",
            description=f"Benchmark client for {self.config.protocol_name} protocol",
            version="1.0.0",
        )

    def _configure_routes(self) -> None:
        """Configure application routes."""

        @self.app.get("/")
        async def root():
            """Health check endpoint."""
            return self._get_health_response()

        @self.app.get("/run-benchmark")
        async def run_benchmark():
            """Execute benchmark."""
            return await self._run_benchmark()

    def _get_health_response(self) -> Dict[str, str]:
        """
        Get health check response.

        Override this method to customize health check response.
        """
        return {
            "service": f"{self.config.protocol_name} Requester",
            "status": "running",
            "protocol": self.config.protocol_name,
            "endpoint": "/run-benchmark",
        }

    async def _run_benchmark(self) -> List[Dict[str, Any]]:
        """
        Execute benchmark with configured number of requests.

        Returns:
            List of benchmark results
        """
        results = []

        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            for i in range(self.config.request_count):
                request_timestamp = datetime.now().isoformat()

                # Send protocol-specific request
                result = await self._send_request(client, request_timestamp)

                # Collect result
                results.append(
                    {
                        "request_id": i,
                        "request_timestamp": result.get("request_timestamp", request_timestamp),
                        "response_timestamp": result.get("response_timestamp"),
                    }
                )

        return results

    async def _send_request(
        self, client: httpx.AsyncClient, request_timestamp: str
    ) -> Dict[str, Any]:
        """
        Send a single benchmark request.

        This method must be implemented by subclasses to provide
        protocol-specific request logic.

        Args:
            client: HTTP client instance
            request_timestamp: Request timestamp in ISO format

        Returns:
            Dictionary with request_timestamp and response_timestamp

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement _send_request()")


# Example usage documentation
"""
Example: REST Requester
-----------------------

from common import BaseBenchmarkRequester, BenchmarkConfig
import httpx
import json

class RestRequester(BaseBenchmarkRequester):
    def __init__(self):
        config = BenchmarkConfig(protocol_name="REST")
        super().__init__(config)

    async def _send_request(self, client, request_timestamp):
        url = f"{self.config.responder_url}/timestamp"

        response = await client.post(
            url,
            json={"request_timestamp": request_timestamp}
        )
        response.raise_for_status()

        return response.json()

# Usage
requester = RestRequester()
app = requester.app

# Run with: uvicorn main:app --host 0.0.0.0 --port 8080
"""
