from pydantic import AwareDatetime, BaseModel


class SchemaBase(BaseModel):
    request_id: int


class SchemaRead(SchemaBase):
    grpc_requester_timestamp: AwareDatetime
    grpc_responder_timestamp: AwareDatetime
