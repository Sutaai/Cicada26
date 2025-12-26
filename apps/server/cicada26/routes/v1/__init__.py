from fastapi import APIRouter

from cicada26.routes.v1.page import router as page_router

router = APIRouter(prefix="/v1")

router.include_router(page_router)
