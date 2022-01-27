from typing import Any, List, Optional
from pydantic.class_validators import validator
from pydantic.fields import Field
from pydantic.main import BaseModel

from herre.access.utils import clean_dict

# Mixin CLass is not Possible because of BaseModel Metaclass


class GraphQLObject(BaseModel):
    def dict(self, *args, by_alias=True, **kwargs):
        return super().dict(
            *args,
            **{
                **kwargs,
                "by_alias": by_alias,
            },
        )

    async def to_variable(self):
        dictionary = self.dict(exclude={"typename"})
        clean_dict(dictionary, lambda key: key == "__typename")
        return dictionary
