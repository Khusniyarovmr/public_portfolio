from pydantic import BaseModel
from sqlalchemy import JSON

class RolesModel(BaseModel):
    name: str
    permission: JSON
    is_enable: int

class RolesCreate(RolesModel):
    pass


class RolesUpdate(RolesModel):
    pass

