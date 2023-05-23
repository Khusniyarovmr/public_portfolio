from sqlalchemy.ext.asyncio import AsyncSession
from src.models.strategy_tp_and_sl import StrategyTpAndSl
from src.schemas.strategy_tp_and_sl import StrategyTPAndSLCreate, StrategyTPAndSLUpdate
from src.services.crud.base import RepositoryDB


class CRUDUStrategyTPAndSL(RepositoryDB[StrategyTpAndSl, StrategyTPAndSLCreate, StrategyTPAndSLUpdate]):

    @staticmethod
    async def add_or_update_tp_and_sl(
            db: AsyncSession,
            obj_in: list[StrategyTPAndSLUpdate]) -> list[StrategyTPAndSLUpdate]:
        list_of_new_obj: list[StrategyTpAndSl] = []
        for obj in obj_in:
            data_obj = StrategyTpAndSl(**obj.dict())
            merged_obj = await db.merge(data_obj)
            await db.commit()
            await db.refresh(merged_obj)
            list_of_new_obj.append(merged_obj)
        return list_of_new_obj


strategy_tp_and_sl_crud = CRUDUStrategyTPAndSL(StrategyTpAndSl)
