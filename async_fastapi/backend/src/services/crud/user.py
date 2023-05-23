from src.models.user import User as UserModel
from src.schemas.users import UserCreate, UserUpdate
from src.services.crud.base import RepositoryDB


class CRUDUser(RepositoryDB[UserModel, UserCreate, UserUpdate]):
    def is_active(self, user: UserModel) -> bool:
        return user.is_active

    def is_superuser(self, user: UserModel) -> bool:
        return user.is_superuser

    def is_autorized(self, user: UserModel) -> bool:
        if user.role_id == 2:
            return True
        return False


user_crud = CRUDUser(UserModel)
