from datetime import UTC, datetime

import grpc
from core.config import settings
from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp
from pb.hello_grpc_pb2 import Request
from pb.hello_grpc_pb2_grpc import GRPCServiceStub


class gRPBResponderClient(object):
    def __init__(self):
        self.channel = grpc.insecure_channel(f"{settings.grpc_responder}:50051")
        # self.channel = grpc.insecure_channel(f"0.0.0.0:50052")
        self.stub = GRPCServiceStub(self.channel)

    def get_ts(self):
        now = datetime.now(UTC)
        request_ts = Timestamp()
        request_ts.FromDatetime(now)

        try:
            stub = self.stub.GetTimestamp(Request(request_ts=request_ts))
            return MessageToDict(stub, preserving_proto_field_name=True), now

        except grpc.RpcError as rpc_error:
            return {"timestamp_status": rpc_error.details()}
