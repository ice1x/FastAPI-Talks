from fastapi import APIRouter

from grpc_requester.api.routes.call_grpc_responder_from_rest import router as restaurants_router

router = APIRouter()


router.include_router(restaurants_router, prefix="/run")
