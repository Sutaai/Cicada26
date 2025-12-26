import typing

import aiofiles
from fastapi import APIRouter, Query, Response
from pydantic import BaseModel

from cicada26.routes.commons import Headers
from cicada26.routes.exceptions import (
    Conflict,
    Forbidden,
    NotFound,
    conflict,
    forbidden,
    notfound,
)
from cicada26.settings import settings
from cicada26.types import ValidSlug

router = APIRouter(prefix="/page", tags=["Page"])


class ExploreDirItem(BaseModel):
    """The relative slug of the page."""

    slug: str
    """Indicates if the slug is of type directory or a page."""
    type: typing.Literal["dir", "page"]


@router.get(
    "/explore",
    response_model=list[ExploreDirItem],
    responses={**notfound("Directory not found")},
)
async def explore_directory(
    directory: typing.Annotated[
        ValidSlug | None,
        Query(
            description=(
                "The path you wish to explore. If none is indicated, the root path will be "
                "explored."
            )
        ),
    ] = None,
) -> list[ExploreDirItem]:
    """
    Explore a directory. This will list all pages availables in a directory.
    This is not recursive, meaning you will have to make a new request to nested directories.

    Specifying no slug will explore the root directory of the wiki.
    """
    if not directory:
        # Reference the top-most folder of the store
        directory = "."

    full_path = (settings.WIKI.STORE / directory).resolve()

    # Not really security by obscurity, just design.
    if not full_path.is_dir() or not full_path.exists():
        raise NotFound(directory, "Directory not found")

    return [
        ExploreDirItem(slug=path.stem, type="dir" if path.is_dir() else "page")
        for path in full_path.iterdir()
    ]


@router.post(
    "/directory",
    status_code=201,
    responses={
        201: {"headers": {**Headers.location("The location of the newly created directory.")}},
        **forbidden("Parent directory does not exist."),
        **conflict("Page or directory already exist at the given location."),
    },
)
async def new_directory(
    slug: typing.Annotated[
        ValidSlug,
        Query(
            description=(
                "The slug to where the directory will be created. The last part of the slug will "
                "be the created directory."
            ),
            examples=["drinks", "drinks/softs", "drinks/non-alcoholic"],
        ),
    ],
):
    """Create a new directory at a specified location."""
    full_path = (settings.WIKI.STORE / slug).resolve()

    try:
        full_path.mkdir()
    except FileExistsError:
        raise Conflict(f"A directory or page already exist at '{slug}'.")
    except FileNotFoundError:
        raise Forbidden(f"No parent folder.")

    return Response(status_code=201, headers={"Location": slug})


@router.post(
    "/page",
    status_code=201,
    responses={
        201: {"headers": {**Headers.location("test")}},
        **forbidden("Parent directory does not exist."),
        **conflict("Page or directory already exist at the given location."),
    },
)
async def new_page(slug: ValidSlug):
    full_path = (settings.WIKI.STORE / slug).with_suffix(".md").resolve()

    try:
        # TODO: Create revision
        full_path.touch(exist_ok=False)
    except FileExistsError:
        raise Conflict("Page already exist.")

    return Response(status_code=201, headers={"Location": slug})


@router.get(
    "/read/{slug:path}",
    responses={**notfound("Page was not found or was pointing to a directory.")},
)
async def get_page(slug: ValidSlug) -> str:
    """Obtain the content of a page in either raw Markdown or rendered HTML."""
    full_path = (settings.WIKI.STORE / slug).with_suffix(".md").resolve()

    if not full_path.is_file() or not full_path.exists():
        raise NotFound(slug, "Page not found")

    async with aiofiles.open(full_path) as file:
        return await file.read()
