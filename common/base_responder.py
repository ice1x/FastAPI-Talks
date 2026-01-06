"""Base class for all benchmark responder services."""

from datetime import datetime
from typing import Any, Callable, Dict, Optional, Protocol

from fastapi import FastAPI, Request, Response

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


class BaseBenchmarkResponder:
    """
    Base class for all benchmark responder services.

    This class provides common functionality for benchmark responders:
    - FastAPI app creation with metadata
    - Health check endpoint
    - Generic timestamp handling logic
    - Response formatting

    Subclasses must implement:
    - _deserialize_request(): Protocol-specific request deserialization
    - _serialize_response(): Protocol-specific response serialization
    """

    def __init__(
        self,
        config: BenchmarkConfig,
        serializer: Serializer,
        deserializer: Deserializer,
        content_type: str = "application/json",
    ):
        """
        Initialize base responder.

        Args:
            config: Benchmark configuration
            serializer: Function to serialize response data
            deserializer: Function to deserialize request data
            content_type: HTTP content type for responses
        """
        self.config = config
        self.serializer = serializer
        self.deserializer = deserializer
        self.content_type = content_type
        self.app = self._create_app()
        self._configure_routes()

    def _create_app(self) -> FastAPI:
        """Create FastAPI application with metadata."""
        return FastAPI(
            title=f"{self.config.protocol_name} Responder Service",
            description=f"Benchmark server for {self.config.protocol_name} protocol",
            version="1.0.0",
        )

    def _configure_routes(self) -> None:
        """Configure application routes."""

        @self.app.get("/")
        async def root():
            """Health check endpoint."""
            return self._get_health_response()

        @self.app.post("/timestamp")
        async def handle_timestamp(request: Request):
            """Handle timestamp request."""
            return await self._handle_timestamp(request)

    def _get_health_response(self) -> Dict[str, str]:
        """
        Get health check response.

        Override this method to customize health check response.
        """
        return {
            "service": f"{self.config.protocol_name} Responder",
            "status": "running",
            "protocol": self.config.protocol_name,
            "message": f"Ready to process {self.config.protocol_name} requests",
        }

    async def _handle_timestamp(self, request: Request) -> Response:
        """
        Handle timestamp request with protocol-specific serialization.

        Args:
            request: FastAPI request object

        Returns:
            FastAPI response with serialized timestamp data
        """
        # Read request body
        body = await request.body()

        # Deserialize using protocol-specific deserializer
        data = self.deserializer(body)

        # Add response timestamp
        data["response_timestamp"] = datetime.now().isoformat()

        # Serialize using protocol-specific serializer
        response_data = self.serializer(data)

        return Response(content=response_data, media_type=self.content_type)


# Example usage documentation
"""
Example: REST Responder
-----------------------

from common import BaseBenchmarkResponder, BenchmarkConfig
import json

class RestResponder(BaseBenchmarkResponder):
    def __init__(self):
        config = BenchmarkConfig(protocol_name="REST")

        # JSON serializer/deserializer
        def serialize(data):
            return json.dumps(data).encode()

        def deserialize(data):
            return json.loads(data)

        super().__init__(
            config=config,
            serializer=serialize,
            deserializer=deserialize,
            content_type="application/json"
        )

# Usage
responder = RestResponder()
app = responder.app

# Run with: uvicorn main:app --host 0.0.0.0 --port 8000
"""
