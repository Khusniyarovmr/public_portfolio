from typing import Any
from sqlalchemy.inspection import inspect
from src.models.user_trade_strategy import UserTradeStrategy
from src.models.signals import Signal
from src.db.redis import st_redis


def publisher(channel: str, data: Any) -> None:
    if isinstance(data, UserTradeStrategy) or isinstance(data, Signal):
        data = clean_data(data)
        del data['create_time']

    if channel == 'strategy_tp_and_sl':
        data = list(map(clean_data, data))

    pub_data = str(data).encode()
    st_redis.publish(channel, pub_data)


def clean_data(data):
    data = inspect(data).dict
    del data['_sa_instance_state']
    return data
