import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class AppSettings(BaseSettings):
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'TestJob_2')
    PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
    PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))
    PASSWORD = str(os.getenv('REDIS_PASSWORD'))
    HOST = str(os.getenv('REDIS_HOST'))
    PORT = str(os.getenv('REDIS_PORT'))
    API_V1_STR: str = "/api/v1"

    app_title: str = PROJECT_NAME


app_settings = AppSettings()
