from typing import Any

import hashlib

from collections.abc import Callable

from starlette.requests import Request
from starlette.responses import Response


def key_builder(
    func: Callable[..., Any],
    namespace: str | None = "",
    request: Request | None = None,  # noqa: ARG001
    response: Response | None = None,  # noqa: ARG001
    args: tuple[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> str:
    """Key builder for fastapi-cache which does not take into account service dependencies.

    See: https://github.com/long2ice/fastapi-cache/issues/279
    """
    from fastapi_cache import FastAPICache

    if kwargs:
        kwargs = {key: value for key, value in kwargs.items() if not key.endswith("_service")}
    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    return (
        prefix
        + hashlib.md5(  # noqa: S324
            f"{func.__module__}:{func.__name__}:{args}:{kwargs}".encode(),
        ).hexdigest()
    )
