from src.crud.base import RepositoryDB
from src.models import Log
from src.schemes.log import LogCreate, LogUpdate


class CRUDLog(RepositoryDB[Log, LogCreate, LogUpdate]):
    pass


log_crud = CRUDLog(Log)
