"""
gRPC Service Endpoint

This module defines the gRPC service that responds to timestamp requests.
It implements the GetTimestamp RPC method defined in the protobuf schema.
"""

from datetime import UTC, datetime

from google.protobuf.timestamp_pb2 import Timestamp

from pb.hello_grpc_pb2 import Response
from pb.hello_grpc_pb2_grpc import GRPCServiceServicer


class BaseServicer(GRPCServiceServicer):
    """
    Base gRPC servicer implementing the GetTimestamp RPC.

    This servicer responds to timestamp requests by returning the current
    server timestamp in UTC format.
    """

    def GetTimestamp(self, request, context):
        """
        Handle GetTimestamp RPC call.

        Args:
            request: The incoming request containing the request timestamp
            context: gRPC context for the call

        Returns:
            Response message containing the server's current timestamp
        """
        now = datetime.now(UTC)
        response_ts = Timestamp()
        response_ts.FromDatetime(now)

        return Response(response_ts=response_ts)
