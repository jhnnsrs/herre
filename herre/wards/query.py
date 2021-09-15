import abc
from herre.loop import loopify
from typing import Any, Dict, List

from pydantic.main import BaseModel
from herre.wards.introspection import Field, Schema, TypeKind
from herre.wards.graphql import ParsedQuery, GraphQLWard
from herre.wards.registry import get_ward_registry

class SchemaException(Exception):
    pass


class QueryResult(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        return self[name]

    def _repr_html_(self):
        return f"<div>Query<div>"



class SchemaRegistry():

    def __init__(self) -> None:
        self.wardSchemaMap: Dict[str, Schema] = {}
        self.wardTypeModelMapMap: Dict[str, Dict[str, BaseModel]] = {}


    def register_model_for_type_and_ward(self, type: str, key: str, model: BaseModel):
        self.wardTypeModelMapMap.setdefault(key, {}).setdefault(type, model)


    async def parse_from_field(self, operation_field: Field, element, ward_key):

        if operation_field.type.kind == TypeKind.LIST:
                if operation_field.type.ofType.kind == TypeKind.OBJECT:
                    model = self.wardTypeModelMapMap[ward_key][operation_field.type.ofType.name]
                    return [model(**el) for el in element]

        elif operation_field.type.kind == TypeKind.OBJECT:
            model = self.wardTypeModelMapMap[ward_key][operation_field.type.name]
            return model(**element)

        raise SchemaException(f"No Object found for this TypeKind {operation_field.type}")


    async def expand_from_schema(self, ward_key, query, result, collapse=False):
        schema = await self.get_schema_for_ward(ward_key)

        parsed_result = {}

        for key, element in result.items():
            operation_name = query.get_operation_name_for_datakey(key)
            operation_field = [field for field in schema.queryType.fields if field.name == operation_name ][0]
            parsed_result[key] = await self.parse_from_field(operation_field, element, ward_key)

        if collapse:
            assert len(parsed_result.items()) == 1, "Cannot collapse query that has more then one operation"
            return parsed_result[query.firstchild]

        return QueryResult(**parsed_result)

        

    async def get_schema_for_ward(self, key: str):
        """Returns the schema for a ward or querys it

        Args:
            key (str): [description]
        """
        if key not in self.wardSchemaMap:
            ward = get_ward_registry().get_ward_instance(key=key)
            assert isinstance(ward, GraphQLWard), "Ward is not of instance GraphQL schemas only supported by GRAPHQL"

            introspection_query = await ward._run_async(ParsedQuery("""
                                    query Schema {
                    __schema {
                        queryType {
                        name
                        description
                        fields {
                            name
                            type {
                            kind
                            ofType {
                                kind
                                name
                                description
                            }
                            name
                            description
                            }
                            description
                            deprecationReason
                        }
                        }
                    }
                    }
            """),{})

            self.wardSchemaMap[key] = Schema(**introspection_query["__schema"])

        return self.wardSchemaMap[key]

CURRENT_SCHEMA_REGISTRY = None

def get_schema_registry():
    global CURRENT_SCHEMA_REGISTRY
    if CURRENT_SCHEMA_REGISTRY is None:
        CURRENT_SCHEMA_REGISTRY = SchemaRegistry()
    return CURRENT_SCHEMA_REGISTRY


class TypedQuery:
    """Generate a query for whatever
    """
    ward_key = None

    def __init__(self, query: str,  ward_key = None, collapse=False) -> None:
        """ A Typed Query

        Typed query takes a querystring and expands it on run from registered
        schemas if the schema is a ward GRAPHQL Sever




        Args:
            query (str): [description]
            ward_key ([type]): [description]
        """
        self.ward_key = ward_key or self.ward_key 
        assert self.ward_key, "Please Specifiy ward key"
        self.ward = get_ward_registry().get_ward_instance(self.ward_key)
        self.query = ParsedQuery(query)
        self.collapse = collapse


    async def _run(self, **variables):
        result = await self.ward._run_async(self.query, variables=variables)
        expanded = await get_schema_registry().expand_from_schema(self.ward_key, self.query, result, collapse=self.collapse)
        return expanded

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.run(**kwds)

    def run(self, **variables):
        return loopify(self._run(**variables))

    def _repr_html_(self):
        return f'<td> <th>Query for Elements {self.ward_key}</th>  <tr> {self.query.firstchild} </tr></td>'





