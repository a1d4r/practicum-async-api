async def get_key_by_args(*args, **kwargs) -> str:
    return f"{args}:{kwargs}"
