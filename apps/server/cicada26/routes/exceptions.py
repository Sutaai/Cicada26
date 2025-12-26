import functools
import typing
from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict


def _openapi_model_schema(title: str, description: str) -> ConfigDict:
    """Return a standard config for exception models.

    Parameters
    ----------
    title : str
        The name of the exception.
    description : str
        A description of the exception

    Returns
    -------
    ConfigDict
        The configuration to pass to `model_config`.
    """
    return ConfigDict({"json_schema_extra": {"title": title, "description": description}})


def _dict_for_response(
    code: int, model: type[BaseModel], description: str
) -> dict[int, dict[str, typing.Any]]:
    """Return a dictionnary to pass directly to a request definition.
    This is used to add additionnal documentation to OpenAPI.

    Parameters
    ----------
    code : int
        The HTTP status code representing the response.
    model : type[BaseModel]
        The model that will be sent accordingly to the status code.
    description : str
        A description of the response.

    Returns
    -------
    dict[int, dict[str, typing.Any]]
        The dictionnary containing the definition of the response.
    """
    return {code: {"model": model, "description": description}}


def _response_description(code: int, model: type[BaseModel]):
    """Return a partial function to dynamically include a description to a response dictionnary.

    Parameters
    ----------
    code : int
        The HTTP status code representing the response.
    model : type[BaseModel]
        The model that will be sent accordingly to the status code.

    Returns
    -------
    partial
        The partial function.
    """
    return functools.partial(_dict_for_response, code, model)


class _BaseOfHTTPException[Detail](BaseModel):
    detail: Detail


class Forbidden(HTTPException):
    def __init__(self, detail: str | None = None) -> None:
        """Raise a forbidden error.

        Parameters
        ----------
        detail : str, optional
            Gives additional detail about the forbidden resource.
            If none, will return a generic "Forbidden" detail.
        """
        super().__init__(HTTPStatus.FORBIDDEN, detail)


class ForbiddenModel(_BaseOfHTTPException[str]):
    """Additionnal detail about the forbidden ressource."""

    model_config: typing.ClassVar[ConfigDict] = _openapi_model_schema(
        "HTTPForbidden",
        "Error indicating a forbidden action. See [Status 403](<https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/403>)",
    )


forbidden = _response_description(HTTPStatus.FORBIDDEN, ForbiddenModel)


class NotFound(HTTPException):
    def __init__(self, input: str | None, info: str) -> None:
        """Raise a not found error.

        Parameters
        ----------
        input : str
            The user's input that led to the error.
        info : str, optional
            Gives additional info about the resource that wasn't found.
        """
        super().__init__(HTTPStatus.NOT_FOUND, {"input": input, "msg": info})


class NotFoundDetailDict(typing.TypedDict):
    input: str | None
    msg: str


class NotFoundModel(_BaseOfHTTPException[NotFoundDetailDict]):
    model_config: typing.ClassVar[ConfigDict] = _openapi_model_schema(
        "HTTPNotFound",
        "Error indicating a not found resource. See [Status 404](<https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/404>)",
    )


notfound = _response_description(HTTPStatus.NOT_FOUND, NotFoundModel)


class Conflict(HTTPException):
    def __init__(self, detail: str | None = None):
        """Raise a conflict error.

        Parameters
        ----------
        detail : str
            Gives additional detail about the conflicting resource.
            If none, will return a generic "Forbidden" detail.
        """
        super().__init__(HTTPStatus.CONFLICT, detail or "Conflicting resource")


class ConflictModel(_BaseOfHTTPException[str]):
    """Additionnal detail about the ressource that conflict."""

    model_config: typing.ClassVar[ConfigDict] = _openapi_model_schema(
        "HTTPConflict",
        "Error indicating a conflicting behavior. See [Status 409](<https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/409>)",
    )


conflict = _response_description(HTTPStatus.CONFLICT, ConflictModel)
