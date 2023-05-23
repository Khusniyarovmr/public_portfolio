import asyncio

from src.core.config import app_settings
from src.db.db import async_session
from src.schemas.symbols import SymbolBase
from src.services.crud.crud_symbols import symbols_crud
from src.services.trading_system.market_api_managers.market_api_base import MarketAPI
from src.services.utilities.utils import Utils


async def get_market_exchange_info() -> None:
    for market in app_settings.stock_markets:
        market_client = get_market_api(market)
        exchange_info = await market_client().get_exchange_info()  # noqa
        cleaned_exchange_info = del_unwanted_elements(market, exchange_info['data'])
        await save_info_in_db(market, cleaned_exchange_info)


def get_market_api(market: str) -> MarketAPI:
    return Utils.get_market_api(market)


async def save_info_in_db(market: str, cleaned_data: list) -> None:
    result_data = []
    for symbol in cleaned_data:
        symbol['stock_market'] = market
        result_data.append(SymbolBase.parse_obj(symbol))
    await symbols_crud.create_multi(
        db=async_session,
        obj_in=result_data
    )


def del_unwanted_elements(market, data: dict) -> list:
    if market == 'Binance':
        cleaned_data = list(map(clean_binance_data, data['symbols']))
    elif market == 'Bybit':
        cleaned_data = []
        pass
    elif market == 'OKX':
        cleaned_data = []
        pass
    else:
        cleaned_data = []
    return cleaned_data


def clean_binance_data(data: dict) -> dict:
    if data.get('underlyingSubType'):
        del data['underlyingSubType']
    if data.get('filters'):
        del data['filters']
    if data.get('orderTypes'):
        del data['orderTypes']
    if data.get('timeInForce'):
        del data['timeInForce']
    return data


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_market_exchange_info())
