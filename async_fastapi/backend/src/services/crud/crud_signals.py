from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.signals import Signal as SignalModel
from src.schemas.signals import SignalsCreate, SignalsUpdate
from src.core.constants import Aliases
from .base import RepositoryDB


class CRUDSignals(RepositoryDB[SignalModel, SignalsCreate, SignalsUpdate]):
    async def new_create(self, db: AsyncSession, *, obj_in: SignalsCreate) -> SignalModel:
        obj_in.point = await self._get_new_point(db, obj_in)
        db_obj = self._model(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def _get_new_point(self, db, data: SignalsCreate):
        sub_stmt = select(func.max(SignalModel.id)).where(SignalModel.symbol == data.symbol, SignalModel.name == data.name)
        stmt = select(SignalModel.point, SignalModel.action).where(SignalModel.id == sub_stmt.scalar_subquery())
        stmt_result = await db.execute(stmt)
        result = stmt_result.fetchone()
        new_point = Aliases.POINT
        if result:
            point, action = result
            match action.upper():
                case Aliases.FLAT | Aliases.CLOSE | Aliases.EXIT:
                    point_split = point.split('_')
                    new_point = point_split[0] + '_' + str(int(point_split[1]) + 1)
                case _:
                    new_point = point
        return new_point


signals_crud = CRUDSignals(SignalModel)


# {
# "name": "cryptobotmain",
# "symbol": "{{ticker}}",
# "price": "{{strategy.order.price}}",
# "action": "{{strategy.order.action}}",
# "type": "{{strategy.market_position}}",
# "lot": "{{strategy.position_size}}"
# }
