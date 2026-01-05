import logging
from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor

from grpc_responder.api.grpc.grpc_endpoint import BaseServicer
from grpc_responder.core.config import settings
from grpc_responder.pb.hello_grpc_pb2_grpc import add_GRPCServiceServicer_to_server


class ResponseTimestampService(BaseServicer):
    pass


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors)
    add_GRPCServiceServicer_to_server(ResponseTimestampService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=settings.logging_level, format=settings.log_format)
    logging.info("gRPC response timestamp Server Starter...")

    serve()
