"""
Tests for gRPC services.
"""

from datetime import datetime

import pytest
from google.protobuf.timestamp_pb2 import Timestamp

from grpc_responder.api.grpc.grpc_endpoint import BaseServicer
from grpc_responder.pb import hello_grpc_pb2


class TestGrpcServicer:
    """Test gRPC servicer functionality."""

    def test_get_timestamp_returns_response(self):
        """Test that GetTimestamp returns a valid Response."""
        servicer = BaseServicer()
        request = hello_grpc_pb2.Request()
        request.request_ts.FromDatetime(datetime.utcnow())

        response = servicer.GetTimestamp(request, None)

        assert isinstance(response, hello_grpc_pb2.Response)
        assert response.response_ts is not None

    def test_get_timestamp_response_has_valid_timestamp(self):
        """Test that the response timestamp is valid and recent."""
        servicer = BaseServicer()
        request = hello_grpc_pb2.Request()
        request.request_ts.FromDatetime(datetime.utcnow())

        before = datetime.utcnow()
        response = servicer.GetTimestamp(request, None)
        after = datetime.utcnow()

        response_time = response.response_ts.ToDatetime()
        assert before <= response_time.replace(tzinfo=None) <= after
