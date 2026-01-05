"""
Business logic for gRPC benchmark execution.

This module handles the execution of gRPC timestamp requests
and assembles the results for benchmark analysis.
"""

from api.dependencies.grpc.call_grpc_responder import gRPBResponderClient
from schemas.metrics import SchemaRead


class RemoteCallLogic:
    """
    Handles the business logic for calling gRPC responder service.

    This class orchestrates the execution of multiple gRPC calls
    and formats the results for benchmark analysis.
    """

    def _get_grpc_responder_timestamp(self, length: int):
        """
        Generate timestamps by calling gRPC responder service.

        Args:
            length: Number of gRPC calls to make

        Yields:
            Tuple of (response_timestamp, request_timestamp) for each call
        """
        for _ in range(length):
            yield gRPBResponderClient().get_ts()

    def build_grpc_metrics(self) -> list[SchemaRead]:
        """
        Execute 1,000 gRPC calls and build metrics list.

        Makes 1,000 sequential gRPC calls to the responder service
        and formats the results into a structured metrics list.

        Returns:
            List of SchemaRead objects containing request IDs and timestamps
        """
        return [
            SchemaRead(
                request_id=request_id,
                grpc_responder_timestamp=metrics[0]["response_ts"],
                grpc_requester_timestamp=metrics[1],
            )
            for request_id, metrics in enumerate(self._get_grpc_responder_timestamp(1000))
        ]
