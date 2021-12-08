from functools import reduce

from pydantic.types import Json


def concat(*args, separator: str = ", ", map_fn = None, filter_fn = None):
    res = separator.join(filter(filter_fn, args))
    return res if map_fn is None else map_fn(res)

def transform(code: str, data: dict, *, search_params: Json):
    data_path, value = code.split("=")

    path = data_path.split(".")
    val = eval(value)

    target = reduce(lambda d, k: d.setdefault(k, {}), path[:-1], data)
    target[path[-1]] = val

    return data
