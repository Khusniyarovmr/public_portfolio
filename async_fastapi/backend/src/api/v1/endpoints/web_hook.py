from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_session
from src.schemas.signals import SignalsCreate
from src.services.crud.crud_signals import signals_crud
from src.services.utilities.publisher import publisher

web_hook_router = APIRouter()


@web_hook_router.post("/web_hook",
                      status_code=200,
                      tags=["webhook"],
                      response_model=SignalsCreate,
                      response_model_exclude_unset=True
                      )
async def web_hook(
        *,
        db: AsyncSession = Depends(get_session),
        entity_in: SignalsCreate,
):
    new_signal = await signals_crud.new_create(db=db, obj_in=entity_in)
    publisher('signal', new_signal)
    return new_signal

# {
# "name": "cryptobotmain",
# "symbol": "{{ticker}}",
# "price": "{{strategy.order.price}}",
# "action": "{{strategy.order.action}}",
# "type": "{{strategy.market_position}}",
# "lot": "{{strategy.position_size}}"
# }

# {
#   "name": "MATICUSDT_new_1",
#   "symbol": "MATICUSDT",
#   "type": "long",
#   "action": "buy",
#   "lot": 3,
#   "price": 1.1543,
#   "point": "string"
# }
