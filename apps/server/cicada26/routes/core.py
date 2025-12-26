import scalar_fastapi as scalar
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def get_scalar(request: Request) -> HTMLResponse:
    return scalar.get_scalar_api_reference(
        openapi_url=request.app.openapi_url, title=request.app.title, theme=scalar.Theme.DEEP_SPACE
    )
