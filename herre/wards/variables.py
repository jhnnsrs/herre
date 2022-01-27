from abc import ABC, abstractmethod
import inspect
import io
from typing import AsyncGenerator, Dict, Tuple, Type, Any
import aiohttp
import xarray as xr

FILE_CLASSES = (
    io.IOBase,
    aiohttp.StreamReader,
    AsyncGenerator,
)


class QueryVariable:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @abstractmethod
    async def to_variable(self):
        raise NotImplementedError


async def parse_variables(
    variables: Dict,
    file_classes: Tuple[Type[Any], ...] = FILE_CLASSES,
    shrinker_funcs={},
    ward=None,
) -> Tuple[Dict, Dict]:
    files = {}

    async def recurse_extract(path, obj):
        """
        recursively traverse obj, doing a deepcopy, but
        replacing any file-like objects with nulls and
        shunting the originals off to the side.
        """
        nonlocal files

        if isinstance(obj, list):
            nulled_obj = []
            for key, value in enumerate(obj):
                value = await recurse_extract(f"{path}.{key}", value)
                nulled_obj.append(value)
            return nulled_obj
        elif isinstance(obj, dict):
            nulled_obj = {}
            for key, value in obj.items():
                value = await recurse_extract(f"{path}.{key}", value)
                nulled_obj[key] = value
            return nulled_obj
        elif isinstance(obj, file_classes):
            # extract obj from its parent and put it into files instead.
            files[path] = obj
            return None

        elif hasattr(obj, "to_variable"):
            return await obj.to_variable()

        else:
            if obj.__class__ in shrinker_funcs:
                return await shrinker_funcs[obj.__class__](obj, ward)
            # base case: pass through unchanged
            return obj

    nulled_variables = await recurse_extract("variables", variables)

    return nulled_variables, files
