from src.models.black_list import BlackList as BlackListModel
from src.schemas.black_list import BlackListCreate, BlackListUpdate
from base import RepositoryDB

class CRUDBlackList(RepositoryDB[BlackListModel, BlackListCreate, BlackListUpdate]):
    pass

black_list_crud = CRUDBlackList(BlackListModel)
