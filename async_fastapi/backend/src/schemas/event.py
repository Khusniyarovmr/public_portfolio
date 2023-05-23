from enum import Enum
from typing import Any

from pydantic import BaseModel


class TypeVariants(str, Enum):
    var_1 = 'delete'
    var_2 = 'modify'
    var_3 = 'control'


class ModifyObject(BaseModel):
    name: str
    data: Any


class EventModel(BaseModel):
    user_id: int
    event_type: TypeVariants
    modify_obj: ModifyObject
