import re
import string
import typing

from pydantic import AfterValidator

ALLOWED_CHARACTERS = set[str](string.ascii_lowercase + string.digits + "/" + "-")
SLUG_REGEX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:\/[a-z0-9]+(?:-[a-z0-9]+)*)*$")
PART_SLUG_REGEX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def valid_raw_slug(input: str) -> str:
    if not SLUG_REGEX.match(input):
        raise ValueError("slug is invalid")

    return input


def valid_raw_part_slug(input: str) -> str:
    if not PART_SLUG_REGEX.match(input):
        raise ValueError("slug is invalid")

    return input


ValidSlug: typing.TypeAlias = typing.Annotated[str, AfterValidator(valid_raw_slug)]
ValidSlugSlashless: typing.TypeAlias = typing.Annotated[str, AfterValidator(valid_raw_part_slug)]
