from src.models.binance_order import BinanceOrder as BinanceOrderModel
from src.schemas.binance_order import BinanceOrderCreate, BinanceOrderUpdate
from src.services.crud.base import RepositoryDB

class CRUDBinanceOrders(RepositoryDB[BinanceOrderModel, BinanceOrderCreate, BinanceOrderUpdate]):
    pass

binance_order_crud = CRUDBinanceOrders(BinanceOrderModel)
