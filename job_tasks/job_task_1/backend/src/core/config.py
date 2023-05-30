import os

from dotenv import load_dotenv
from pydantic import BaseSettings
from sqlalchemy.engine.url import URL

load_dotenv()


class AppSettings(BaseSettings):
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'SearchNearestTruck')
    PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
    PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))
    DATABASE = str(os.getenv('DATABASE'))
    DB_USER = str(os.getenv('DB_USER'))
    PASSWORD = str(os.getenv('PASSWORD'))
    DRIVER = str(os.getenv('DRIVER'))
    HOST = str(os.getenv('HOST'))
    PORT = str(os.getenv('PORT'))
    API_V1_STR: str = "/api/v1"

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


app_settings = AppSettings()
