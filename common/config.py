"""Shared configuration constants for all benchmark services."""

from typing import Final

# Request configuration
REQUEST_COUNT: Final[int] = 1000
TIMEOUT_SECONDS: Final[int] = 30

# Service ports
DEFAULT_RESPONDER_PORT: Final[int] = 8000
DEFAULT_REQUESTER_PORT: Final[int] = 8080
GRPC_PORT: Final[int] = 50051

# URLs
LOCALHOST: Final[str] = "127.0.0.1"


class BenchmarkConfig:
    """Configuration for benchmark services."""

    def __init__(
        self,
        protocol_name: str,
        responder_port: int = DEFAULT_RESPONDER_PORT,
        requester_port: int = DEFAULT_REQUESTER_PORT,
        request_count: int = REQUEST_COUNT,
        timeout: int = TIMEOUT_SECONDS,
    ):
        self.protocol_name = protocol_name
        self.responder_port = responder_port
        self.requester_port = requester_port
        self.request_count = request_count
        self.timeout = timeout

    @property
    def responder_url(self) -> str:
        """Get responder base URL."""
        return f"http://{LOCALHOST}:{self.responder_port}"

    @property
    def requester_url(self) -> str:
        """Get requester base URL."""
        return f"http://{LOCALHOST}:{self.requester_port}"
