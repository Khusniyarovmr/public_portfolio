from src.models.user_trading_status import UserTradingStatus
from src.schemas.user_trading_status import UserTradingStatusCreate, UserTradingStatusUpdate
from base import RepositoryDB

class CRUDUserTradingStatus(RepositoryDB[UserTradingStatus, UserTradingStatusCreate, UserTradingStatusUpdate]):
    pass

user_trading_status_crud = CRUDUserTradingStatus(UserTradingStatus)
