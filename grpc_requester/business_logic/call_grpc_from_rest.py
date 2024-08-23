from schemas.metrics import SchemaRead
from api.dependencies.grpc.call_grpc_responder import gRPBResponderClient


class RemoteCallLogic:
    def _get_grpc_responder_timestamp(self, length: int):
        for _ in range(length):
            yield gRPBResponderClient().get_ts()

    def build_grpc_metrics(self) -> SchemaRead:
        return [
            SchemaRead(
                request_id=request_id,
                grpc_responder_timestamp=metrics[0]["response_ts"],
                grpc_requester_timestamp=metrics[1])
            for request_id, metrics in enumerate(self._get_grpc_responder_timestamp(1000))
        ]
