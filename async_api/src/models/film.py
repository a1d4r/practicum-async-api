from typing import Any

from collections.abc import Callable

import orjson

from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Callable[[Any], Any]) -> bytes:
    return orjson.dumps(v, default=default)


class Film(BaseModel):
    id: str
    title: str
    description: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
