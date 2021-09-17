from herre.wards.variables import QueryVariable
from typing import Any, List, Optional
from pydantic.class_validators import validator
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.error_wrappers import ValidationError
from herre.wards.graphql import ParsedQuery, GraphQLWard
from herre.wards.query import get_schema_registry
from herre.access.model.base import AsyncModelManager, SyncModelManager, Model, ModelType
import logging

logger = logging.getLogger(__name__)

class GraphQLExpansionError(Exception):
    pass


class GraphQLSyncModelManager(SyncModelManager):

    def from_query(self, query, **kwargs):
        res_dict =  self.ward._run_sync(query, variables=kwargs)
        return self.modelClass(**res_dict[query.firstchild])


    def get(self, **kwargs) -> ModelType:
        return self.from_query(self.modelClass.Meta.get, **kwargs)

    def create(self, **kwargs) -> ModelType:
        return self.from_query(self.modelClass.Meta.create, **kwargs)


    
class GraphQLAsyncModelManager(AsyncModelManager):


    async def from_query(self, query, **kwargs):
        res_dict =  await self.ward._run_async(query, variables=kwargs)
        return self.modelClass(**res_dict[query.firstchild])
    
    async def get(self, **kwargs) -> ModelType:
        return await self.from_query(self.modelClass.Meta.get, **kwargs)

    async def create(self, **kwargs) -> ModelType:
        return await self.from_query(self.modelClass.Meta.create, **kwargs)


        

# Mixin CLass is not Possible because of BaseModel Metaclass
class GraphQLObject(BaseModel):
    typename: Optional[str] = Field(alias="__typename")

    def __init__(__pydantic_self__, **data: Any) -> None:
        if "__typename" not in data: data["__typename"] = __pydantic_self__.__class__.__name__ 
        super().__init__(**data)

    @validator('typename')
    def typename_matches_class(cls, v):
        if v is None: return None # We are ommiting typechecks if __typename is not explicitly set
        if cls.__name__ == v: return v
        raise ValueError(f"Didn't find correct class {cls.__name__} __typename {v}")

    def dict(self, *args, by_alias=True, **kwargs):
        return super().dict(*args, **{
            **kwargs,
            "by_alias": by_alias,
        })

    


class GraphQLModel(Model, QueryVariable):
    typename: Optional[str] = Field(alias="__typename")


    def __init__(__pydantic_self__, **data: Any) -> None:
        if "__typename" not in data: data["__typename"] = __pydantic_self__.__class__.__name__ 
        try:
            super().__init__(**data)
        except ValidationError as e:
            raise GraphQLExpansionError(f"Couldn't expand {data} ") from e
            


    @validator('typename')
    def typename_matches_class(cls, v):
        if v is None: return None # We are ommiting typechecks if __typename is not explicitly set
        if cls.__name__ == v: return v
        raise ValueError(f"Didn't find correct class {cls.__name__} __typename {v}")

    def dict(self, *args, as_input=False, **kwargs):
        return super().dict(*args, **{
            **kwargs,
            "by_alias": not as_input,
        })

    @classmethod
    def register_model(cls, meta=None):
        registered_typename = getattr(meta, "typename", cls.__name__)
        get_schema_registry().register_model_for_type_and_ward(registered_typename, meta.ward, cls)


    async def to_variable(self):
        return self.id

    @classmethod
    def get_objectsclass(cls):
        return GraphQLSyncModelManager

    @classmethod
    def get_asyncclass(cls):
        return GraphQLAsyncModelManager

    @property
    def ward(self) -> GraphQLWard:
        return self.__class__.asyncs.ward

    class Meta:
        abstract = True