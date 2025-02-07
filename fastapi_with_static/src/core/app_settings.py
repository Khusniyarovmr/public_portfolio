import pathlib

from pydantic.v1 import BaseSettings


class AppSettings(BaseSettings):
    BASE_DIR: str = str(pathlib.Path(__file__).parent.parent.parent)
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    class Config:
        env_file = ".env"


app_settings = AppSettings()  # noqa
