from datetime import datetime, timedelta
from typing import Any, Union

from fastapi_csrf_protect import CsrfProtect
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.core.config import app_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def secure_api_secret(
        subject: Union[str, Any], expires_delta: int
) -> str:
    expire = datetime.utcnow() + timedelta(days=expires_delta)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, app_settings.STOCK_KEY_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def secure_api_key(
        subject: Union[str, Any], expires_delta: int
) -> str:
    expire = datetime.utcnow() + timedelta(days=expires_delta)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, app_settings.STOCK_API_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_stock_api_key(
        token: str
) -> dict:
    decoded_jwt = jwt.decode(token, app_settings.STOCK_API_KEY, algorithms=ALGORITHM)
    return decoded_jwt


def decode_stock_api_secret(
        token: str
) -> dict:
    decoded_jwt = jwt.decode(token, app_settings.STOCK_KEY_SECRET, algorithms=ALGORITHM)
    return decoded_jwt


def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, app_settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class CsrfSettings(BaseModel):
    secret_key: str = app_settings.CSRF_SECRET


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()
