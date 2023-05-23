from src.models.user_account_info import UserAccountInfo
from src.schemas.user_account_info import UserAccountInfoCreate, UserAccountInfoUpdate
from base import RepositoryDB

class CRUDUserAccountInfo(RepositoryDB[UserAccountInfo, UserAccountInfoCreate, UserAccountInfoUpdate]):
    pass

user_account_info_crud = CRUDUserAccountInfo(UserAccountInfo)
