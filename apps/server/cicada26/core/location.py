"""
This module implements the Location class.

This class is used to reference paths in the application.
They take the form of slugs.
"""

import pathlib

from cicada26.settings import settings


class Location:
    def __init__(self, slug: str):
        self.path: pathlib.Path = settings.WIKI.STORE / slug

    @property
    def is_directory(self):
        return self.path.is_dir()

    @property
    def is_page(self):
        return self.path.is_file()
