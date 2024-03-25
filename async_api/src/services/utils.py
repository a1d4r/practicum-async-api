def get_key_by_args(*args: str, **kwargs: str) -> str:
    return f"{args}:{kwargs}"
