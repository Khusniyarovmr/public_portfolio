from src.models.roles import Role as RoleModel
from src.schemas.roles import RolesCreate, RolesUpdate
from base import RepositoryDB

class CRUDRoles(RepositoryDB[RoleModel, RolesCreate, RolesUpdate]):
    pass

roles_crud = CRUDRoles(RoleModel)
