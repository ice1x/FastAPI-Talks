from fastapi import APIRouter, Depends

from grpc_requester.business_logic.call_grpc_from_rest import RemoteCallLogic
from grpc_requester.schemas.metrics import SchemaRead

router = APIRouter()


@router.get(
    "",
    status_code=201,
    name="call_nested_grpc",
    response_model=list[SchemaRead],
    responses={422: {"model": SchemaRead}},
)
def get_grpc_responder_timestamp(
    grpc_call_logic: RemoteCallLogic = Depends(RemoteCallLogic),
) -> SchemaRead:
    return grpc_call_logic.build_grpc_metrics()
