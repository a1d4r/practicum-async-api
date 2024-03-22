from typing import Any


def get_key_by_args(*args: Any, **kwargs: Any) -> str:
    return f"{args}:{kwargs}"
