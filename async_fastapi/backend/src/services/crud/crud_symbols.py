from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime

from src.services.crud.base import RepositoryDB
from src.models.symbols import Symbol as SymbolModel
from src.schemas.symbols import SymbolCreate, SymbolUpdate


class CRUDSymbols(RepositoryDB[SymbolModel, SymbolCreate, SymbolUpdate]):

    async def create_multi(self, db: AsyncSession, *, obj_in: list) -> None:
        async with db.begin() as session:
            for obj in obj_in:
                stmt = insert(SymbolModel).values(
                    symbol=obj.symbol,
                    stock_market=obj.stock_market,
                    pair=obj.pair,
                    status=obj.status,
                    price_precision=obj.pricePrecision,
                    quantity_precision=obj.quantityPrecision,)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[SymbolModel.symbol, SymbolModel.stock_market],
                    index_where=(SymbolModel.symbol == obj.symbol)
                    & (SymbolModel.stock_market == obj.stock_market),
                    set_=dict(update_date=datetime.utcnow(),
                              pair=stmt.excluded.pair,
                              status=stmt.excluded.status,
                              price_precision=stmt.excluded.price_precision,
                              quantity_precision=stmt.excluded.quantity_precision
                              )
                )
                await session.execute(stmt)


symbols_crud = CRUDSymbols(SymbolModel)
