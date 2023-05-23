from fastapi_users.authentication import AuthenticationBackend
from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import JWTStrategy

from src.core.config import app_settings

SECRET = app_settings.JWT_SECRET

cookie_transport = CookieTransport(
    cookie_max_age=3600,
    cookie_httponly=True,
    cookie_name='cryptotradecook',
    cookie_samesite='lax',
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


cookie_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
