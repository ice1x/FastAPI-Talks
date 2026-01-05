from datetime import UTC, datetime

from grpc_responder.pb.hello_grpc_pb2 import Request


def get_utc_now():
    return datetime.now(UTC).timestamp()


def test_get_timestamp(grpc_stub):
    request = Request()
    ts_before = get_utc_now()
    response = grpc_stub.GetTimestamp(request)
    ts_after = get_utc_now()
    timestamp_dt = datetime.fromtimestamp(
        response.response_ts.seconds + response.response_ts.nanos / 1e9
    ).timestamp()
    assert ts_before < timestamp_dt < ts_after
