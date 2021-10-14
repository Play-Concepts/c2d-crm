from functools import reduce

from pydantic.types import Json


def concat(*args, separator: str = ", "):
    return separator.join(filter(None, args))


def transform(code: str, data: dict, *, search_params: Json):
    data_path, value = code.split("=")

    path = data_path.split(".")
    val = eval(value)

    target = reduce(lambda d, k: d.setdefault(k, {}), path[:-1], data)
    target[path[-1]] = val

    return data
