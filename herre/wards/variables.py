from abc import ABC, abstractmethod

class QueryVariable:

    @abstractmethod
    async def to_variable(self):
        raise NotImplementedError



async def parse_variables(variables):

    parsed_kwargs = {}

    for key, value in variables.items():
        if isinstance(value, QueryVariable):
            parsed_kwargs[key] = await value.to_variable()
        else:
            parsed_kwargs[key] = value


    return parsed_kwargs