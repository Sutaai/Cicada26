from fastapi.routing import APIRouter

from cicada26.routes.core import router as core_router
from cicada26.routes.v1 import router as v1_core_router

api_router = APIRouter(prefix="/api")
api_router.include_router(core_router)
api_router.include_router(v1_core_router)
