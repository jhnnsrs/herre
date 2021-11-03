from abc import ABC, abstractmethod
import inspect


class QueryVariable:
    @abstractmethod
    async def to_variable(self):
        raise NotImplementedError


async def parse_variables(variables):
    print(variables)
    parsed_kwargs = {}

    for key, value in variables.items():
        if hasattr(value, "to_variable"):
            print("nanan")
            parsed_kwargs[key] = await value.to_variable()
        else:
            parsed_kwargs[key] = value

    return parsed_kwargs
