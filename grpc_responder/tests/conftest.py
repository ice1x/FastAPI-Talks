import pytest


@pytest.fixture(scope="module")
def grpc_add_to_server():
    from pb.hello_grpc_pb2_grpc import add_GRPCServiceServicer_to_server

    return add_GRPCServiceServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer():
    from api.grpc.grpc_endpoint import BaseServicer

    return BaseServicer()


@pytest.fixture(scope="module")
def grpc_stub_cls(grpc_channel):
    from pb.hello_grpc_pb2_grpc import GRPCServiceStub

    return GRPCServiceStub
