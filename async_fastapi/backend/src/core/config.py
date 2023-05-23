import os

from dotenv import load_dotenv
from pydantic import BaseSettings
from sqlalchemy.engine.url import URL

load_dotenv()


class AppSettings(BaseSettings):
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'CryptoTrading')
    PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
    PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))
    DATABASE = str(os.getenv('DATABASE'))
    DB_USER = str(os.getenv('DB_USER'))
    PASSWORD = str(os.getenv('PASSWORD'))
    DRIVER = str(os.getenv('DRIVER'))
    HOST = str(os.getenv('HOST'))
    PORT = os.getenv('PORT')
    JWT_SECRET: str = os.getenv('JWT_SECRET')
    TELEGRAM_TOKEN: str = os.getenv('TELEGRAM_TOKEN')
    API_V1_STR: str = "/api/v1"
    CSRF_SECRET: str = os.getenv('CSRF_SECRET')
    STOCK_KEY_SECRET: str = os.getenv('STOCK_KEY_SECRET')
    STOCK_API_KEY: str = os.getenv('STOCK_API_KEY')

    posgtres_url = URL.create(
        drivername=DRIVER,
        username=DB_USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DATABASE,
    )

    app_title: str = PROJECT_NAME
    database_dsn: URL = posgtres_url

    stock_markets = ['Binance',
                     # 'Bybit',
                     # 'OKX'
                     ]


app_settings = AppSettings()
