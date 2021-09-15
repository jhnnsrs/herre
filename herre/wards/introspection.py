from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum

from typing import ForwardRef



class TypeKind(str, Enum):
    SCALAR = "SCALAR"
    OBJECT = "OBJECT"
    LIST = "LIST"
    INTERFACE = "INTERFACE"
    UNION = "UNION"
    ENUM = "ENUM"
    INPUT_OBJECT = "INPUT_OBJECT"
    NON_NULL = "NON_NULL"


Type = ForwardRef("Type")
InputValue = ForwardRef("InputValue")
Field = ForwardRef("Field")

class InputValue(BaseModel):
    name: Optional[str]
    description: Optional[str]
    type: Optional[Type]
    defaultValue: Optional[str]


class Field(BaseModel):
    name: Optional[str]
    description:  Optional[str]
    args: Optional[List[InputValue]]
    type: Optional[Type]
    isDeprecated: Optional[bool]
    deprecationReason: Optional[bool]


class Type(BaseModel):
    kind: Optional[TypeKind]
    description: Optional[str]
    name: Optional[str]
    fields: Optional[List[Field]]
    interfaces:  Optional[List[Type]]
    inputFields:  Optional[List[InputValue]]
    ofType: Optional[Type]



Type.update_forward_refs()
InputValue.update_forward_refs()
Field.update_forward_refs()


class Schema(BaseModel):
    types: Optional[List[Type]]
    queryType: Optional[Type]
