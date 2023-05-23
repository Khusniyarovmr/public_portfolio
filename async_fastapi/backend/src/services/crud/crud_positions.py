from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.positions import Position as PositionModel
from src.schemas.positions import PositionCreate, PositionUpdate
from src.services.crud.base import RepositoryDB


class CRUDPositions(RepositoryDB[PositionModel, PositionCreate, PositionUpdate]):
    @staticmethod
    async def upinsert(db: AsyncSession, *, obj_in: PositionUpdate) -> None:
        stmt = insert(PositionModel).values(
            user_id=obj_in.user_id,
            stock_market=obj_in.stock_market,
            signal_name=obj_in.signal_name,
            strategy_id=obj_in.strategy_id,
            create_time=obj_in.create_time,
            close_time=obj_in.close_time,
            symbol_id=obj_in.symbol_id,
            side=obj_in.side,
            lot=obj_in.lot,
            first_order_lot=obj_in.first_order_lot,
            open_price=obj_in.open_price,
            close_price=obj_in.close_price,
            point=obj_in.point,
            status=obj_in.status,
            count=obj_in.count)
        stmt = stmt.on_conflict_do_update(
            index_elements=[PositionModel.user_id,
                            PositionModel.strategy_id,
                            PositionModel.symbol_id,
                            PositionModel.signal_name,
                            PositionModel.stock_market],
            index_where=(PositionModel.user_id == obj_in.user_id)
                    & (PositionModel.strategy_id == obj_in.strategy_id)
                    & (PositionModel.symbol_id == obj_in.symbol_id)
                    & (PositionModel.signal_name == obj_in.signal_name)
                    & (PositionModel.stock_market == obj_in.stock_market),
            set_=dict(
                      close_time=stmt.excluded.close_time,
                      side=stmt.excluded.side,
                      lot=stmt.excluded.lot,
                      first_order_lot=stmt.excluded.first_order_lot,
                      open_price=stmt.excluded.open_price,
                      close_price=stmt.excluded.close_price,
                      point=stmt.excluded.point,
                      status=stmt.excluded.status,
                      count=stmt.excluded.count
                      )
        )
        await db.execute(stmt)
        await db.commit()


positions_crud = CRUDPositions(PositionModel)
