from api.routes.call_grpc_responder_from_rest import router as restaurants_router
from fastapi import APIRouter

router = APIRouter()


router.include_router(restaurants_router, prefix="/run")
