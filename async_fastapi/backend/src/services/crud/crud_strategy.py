from src.models.strategy import Strategy as StrategyModel
from src.schemas.strategy import StrategyCreate, StrategyUpdate
from src.services.crud.base import RepositoryDB

class CRUDStrategy(RepositoryDB[StrategyModel, StrategyCreate, StrategyUpdate]):
    pass

strategy_crud = CRUDStrategy(StrategyModel)
