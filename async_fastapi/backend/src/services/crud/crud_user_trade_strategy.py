from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user_trade_strategy import UserTradeStrategy
from src.schemas.user_trade_strategy import UserTradeStrategyCreate, UserTradeStrategyUpdate
from src.services.crud.base import RepositoryDB


class CRUDUserTradeStrategy(RepositoryDB[UserTradeStrategy, UserTradeStrategyCreate, UserTradeStrategyUpdate]):
    async def get_all_active_strategies(self, db: AsyncSession, user_id: int) -> List[UserTradeStrategy]:
        statement = select(UserTradeStrategy).filter(UserTradeStrategy.user_id == user_id,
                                                     UserTradeStrategy.is_active == 1)
        results = await db.execute(statement=statement)
        return results.scalars().all()

    async def get_all_strategies(self, db: AsyncSession, user_id: int) -> List[UserTradeStrategy]:
        statement = select(UserTradeStrategy).filter(UserTradeStrategy.user_id == user_id)
        results = await db.execute(statement=statement)
        return results.scalars().all()


user_trade_strategy_crud = CRUDUserTradeStrategy(UserTradeStrategy)
