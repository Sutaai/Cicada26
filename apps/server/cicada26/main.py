import contextlib
import logging

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse

from cicada26.meta import __version__
from cicada26.routes import api_router
from cicada26.settings import settings

_log = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI):
    # Create the store folder if necessary.
    base_folder = settings.WIKI.STORE
    if not base_folder.exists():
        base_folder.mkdir()
        _log.warning("Store folder has been created.")
    yield


app = FastAPI(title=settings.WIKI.NAME, docs_url=None, redoc_url=None, lifespan=lifespan)
app.include_router(api_router)


@app.get("/", include_in_schema=False)
def redir_to_docs() -> RedirectResponse:
    return RedirectResponse("/api/docs")


app.openapi_schema = get_openapi(
    title=settings.WIKI.NAME,
    summary=f"Complete documentation of the API of {settings.WIKI.NAME}.\nPowered by Cicada26.",
    version=__version__,
    routes=app.routes,
)
