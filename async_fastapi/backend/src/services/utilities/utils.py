import ast
from src.services.trading_system.market_api_managers.market_api_base import MarketAPI
from src.services.trading_system.market_api_managers.data_prepare_base import DataPreparationModel
import src.services.trading_system.market_api_managers.market_api_initialization  # noqa
from src.core.security import decode_stock_api_secret, decode_stock_api_key
from src.schemas.user_settings import UserSettingsInfo


class Utils:
    @staticmethod
    def make_dict_from_literal(data: str) -> list | dict | str:
        try:
            result = ast.literal_eval(data)
        except ValueError:
            result = data
        return result

    @staticmethod
    def get_market_api(stock_market: str) -> MarketAPI | None:
        classes = MarketAPI.__subclasses__()
        market_api_class = None
        for clas in classes:
            if stock_market.upper() in clas.__name__.upper():
                market_api_class = clas
                break
        return market_api_class

    @staticmethod
    def get_data_prep_market(stock_market: str) -> DataPreparationModel | None:
        classes = DataPreparationModel.__subclasses__()
        data_prep_class = None
        for clas in classes:
            if stock_market.upper() in clas.__name__.upper():
                data_prep_class = clas
                break
        return data_prep_class

    @staticmethod
    def get_user_market_info(user: int, user_info: UserSettingsInfo | dict, market: str) -> tuple:
        if isinstance(user_info, dict):
            api_info = list(filter(lambda x: x.stock_market == market, user_info[user]))[0]
        else:
            api_info = user_info
        api_key = decode_stock_api_key(api_info.hashed_key)
        api_secret = decode_stock_api_secret(api_info.hashed_secret)
        return api_key['sub'], api_secret['sub']
