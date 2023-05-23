import asyncio
from collections import defaultdict

from sqlalchemy import select, distinct
from sqlalchemy.inspection import inspect
from sqlalchemy.sql.expression import true  # noqa
from sqlalchemy.sql.functions import max

from src.db.db import async_session
from src.db.redis import aio_redis as redis
from src.models.black_list import BlackList
from src.models.signals import Signal
from src.models.strategy_tp_and_sl import StrategyTpAndSl
from src.models.symbols import Symbol
from src.models.user import User
from src.models.user_settings import UserSettings
from src.models.user_trade_strategy import UserTradeStrategy
from src.models.user_trading_status import UserTradingStatus
from src.schemas.signals import SignalStatus
from src.schemas.strategy_tp_and_sl import StrategyTPAndSLModel
from src.schemas.symbols import SymbolTradeInfo
from src.schemas.user_settings import UserSettingsInfo
from src.schemas.user_trade_strategy import UserTradeStrategyWithSymbol

ACTIVE_TRADERS_STMT = select(distinct(UserTradingStatus.user_id)).join(User,
                                                                       UserTradingStatus.user_id == User.id).where(
    # noqa
    UserTradingStatus.status == true(), User.role_id == 2)


class CRUDInitialData:

    @staticmethod
    async def get_active_traders():
        result = []
        async with async_session.begin() as session:
            stmt_data = await session.execute(ACTIVE_TRADERS_STMT)
            data = stmt_data.fetchall()
        if data:
            for user_id in data:
                result.append(user_id[0])
            await redis.sadd('activeTraders', *result)
        return result

    @staticmethod
    async def get_user_black_list():
        result = defaultdict(list)
        stmt = select(BlackList.user_id, Symbol.symbol)
        stmt = stmt.join(Symbol, BlackList.symbol_id == Symbol.id)  # noqa
        stmt = stmt.where(BlackList.user_id == ACTIVE_TRADERS_STMT.scalar_subquery(),
                          BlackList.is_enable == 1)
        async with async_session.begin() as session:
            stmt_data = await session.execute(stmt)
            data = stmt_data.fetchall()
        if data:
            for user_id, symbol in data:
                result[user_id].append(symbol)
        return result

    @staticmethod
    async def get_list_of_strategy_id_per_user():
        result = defaultdict(list)  # noqa
        stmt = select(UserTradeStrategy.user_id, UserTradeStrategy.id)  # noqa
        stmt = stmt.where(UserTradeStrategy.user_id == ACTIVE_TRADERS_STMT.scalar_subquery(),
                          UserTradeStrategy.is_active == 1)
        async with async_session.begin() as session:
            stmt_data = await session.execute(stmt)
            data = stmt_data.fetchall()
        if data:
            for user_id, strategy_id in data:
                result[user_id].append(strategy_id)
        return result

    @staticmethod
    async def get_list_of_strategy_id_per_signal_name():
        result = defaultdict(list)  # noqa
        stmt = select(UserTradeStrategy.signal_name, UserTradeStrategy.id)  # noqa
        stmt = stmt.where(UserTradeStrategy.user_id == ACTIVE_TRADERS_STMT.scalar_subquery(),
                          UserTradeStrategy.is_active == 1)
        async with async_session.begin() as session:
            stmt_data = await session.execute(stmt)
            data = stmt_data.fetchall()
        if data:
            for signal_name, strategy_id in data:
                result[signal_name].append(strategy_id)
        return result

    @staticmethod
    async def get_strategy_info():
        result = {}
        stmt = select(UserTradeStrategy.id, UserTradeStrategy, Symbol.symbol)
        stmt = stmt.join(Symbol, UserTradeStrategy.symbol_id == Symbol.id)  # noqa
        stmt = stmt.where(UserTradeStrategy.user_id == ACTIVE_TRADERS_STMT.scalar_subquery(),
                          UserTradeStrategy.is_active == 1)
        async with async_session.begin() as session:
            stmt_data = await session.execute(stmt)
            data = stmt_data.fetchall()
        if data:
            for strategy_id, strategy_model_obj, symbol in data:
                strategy_dict = inspect(strategy_model_obj).dict
                del strategy_dict['_sa_instance_state']
                strategy_dict['symbol'] = symbol
                result[strategy_id] = UserTradeStrategyWithSymbol.parse_obj(strategy_dict)
                redis_result = UserTradeStrategyWithSymbol.parse_obj(strategy_dict).json()
                await redis.hset(name='strategyInfo', key=strategy_id, value=redis_result)
        return result

    @staticmethod
    async def get_strategy_tp_and_sl():
        result = defaultdict(list)
        stmt = select(UserTradeStrategy.id, StrategyTpAndSl)
        stmt = stmt.join(UserTradeStrategy, UserTradeStrategy.id == StrategyTpAndSl.strategy_id)  # noqa
        stmt = stmt.where(UserTradeStrategy.user_id == ACTIVE_TRADERS_STMT.scalar_subquery(),
                          UserTradeStrategy.is_active == 1)
        async with async_session.begin() as session:
            stmt_data = await session.execute(stmt)
            data = stmt_data.fetchall()
        if data:
            for strategy_id, tp_and_sl_object in data:
                strategy_dict = inspect(tp_and_sl_object).dict
                del strategy_dict['_sa_instance_state']
                result[strategy_id].append(StrategyTPAndSLModel.parse_obj(strategy_dict))
        return result

    @staticmethod
    async def get_symbol_info():
        result = {}
        stmt = select(Symbol.stock_market, Symbol.symbol, Symbol.price_precision, Symbol.quantity_precision)
        async with async_session.begin() as session:
            stmt_data = await session.execute(stmt)
            data = stmt_data.fetchall()
        if data:
            for stock_market, symbol, pricePrecision, quantityPrecision in data:
                data_row = SymbolTradeInfo(pricePrecision=pricePrecision,
                                           quantityPrecision=quantityPrecision)
                result[(stock_market, symbol)] = data_row
                redis_key = str(stock_market+symbol)
                await redis.hset(name='symbolInfo', key=redis_key, value=data_row.json())
        return result

    @staticmethod
    async def get_signal_status():
        result = {}
        sub_stmt = select(Signal.name, Signal.symbol, max(Signal.id).label('max_id')).group_by(Signal.name,
                                                                                               Signal.symbol).subquery()
        stmt = select(Signal.name, Signal.symbol, Signal.type, Signal.action, Signal.point)
        stmt = stmt.join(sub_stmt, Signal.id == sub_stmt.c.max_id)

        async with async_session.begin() as session:
            stmt_data = await session.execute(stmt)
            data = stmt_data.fetchall()
        if data:
            for name, symbol, signal_type, action, point in data:
                result[(name, symbol)] = SignalStatus(type=signal_type, action=action, point=point)
        return result

    @staticmethod
    async def get_user_info():
        result = defaultdict(list)
        stmt = select(UserSettings.user_id,
                      UserSettings.stock_market,
                      UserSettings.hashed_key,
                      UserSettings.hashed_secret)
        stmt = stmt.where(UserSettings.user_id == ACTIVE_TRADERS_STMT.scalar_subquery(),
                          UserSettings.is_active == 1, UserSettings.is_enable == 1)

        async with async_session.begin() as session:
            stmt_data = await session.execute(stmt)
            data = stmt_data.fetchall()
        if data:
            for user_id, market, key, secret in data:
                data_row = UserSettingsInfo(stock_market=market,
                                            hashed_key=key,
                                            hashed_secret=secret)
                result[user_id].append(data_row)
                redis_key = str(market+str(user_id))
                await redis.hset(name='userMarketInfo', key=redis_key, value=data_row.json())
        return result


get_initial_data = CRUDInitialData()

if __name__ == '__main__':
    asyncio.run(get_initial_data.get_active_traders())
