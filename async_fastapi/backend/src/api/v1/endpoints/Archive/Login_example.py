from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_users import models
from fastapi_users.authentication import Authenticator, BaseAuthentication
from fastapi_users.db import BaseUserDatabase
from fastapi_users.router.common import ErrorCode


def get_auth_router(
    backend: BaseAuthentication,
    user_db: BaseUserDatabase[models.BaseUserDB],
    authenticator: Authenticator,
) -> APIRouter:
    """Generate a router with login/logout routes for an authentication backend."""
    router = APIRouter()

    @router.post("/login")
    async def login(
        # Ask for the two fields in the request
        response: Response, email: str = Form(), password: str = Form()
    ):
        # Manually instantiate an `OAuth2PasswordRequestForm` with their values
        credentials = OAuth2PasswordRequestForm(username=email, password=password)
        user = await user_db.authenticate(credentials)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )

        return await backend.get_login_response(user, response)

    if backend.logout:

        @router.post("/logout")
        async def logout(
            response: Response, user=Depends(authenticator.get_current_active_user)
        ):
            return await backend.get_logout_response(user, response)

    return router


# Before
auth_router = fastapi_users.get_auth_router(jwt_authentication)

# After
auth_router = get_auth_router(jwt_authentication, user_db, fastapi_users.authenticator)
