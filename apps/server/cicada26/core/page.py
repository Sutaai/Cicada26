import pathlib

import aiofiles

from cicada26.settings import settings
from cicada26.types import valid_raw_slug


class Page:
    def __init__(self, slug: str):
        if not valid_raw_slug(slug):
            raise ValueError("slug is not of valid format")

        self.path: pathlib.Path = (settings.WIKI.STORE / slug).resolve()

    @property
    def slug(self) -> str:
        return self.path.stem

    async def write_content(self, content: str):
        async with aiofiles.open(self.path) as file:
            return await file.write(content)

    async def read_content(self) -> str:
        async with aiofiles.open(self.path) as file:
            return await file.read()
