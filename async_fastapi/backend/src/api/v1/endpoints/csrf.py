from fastapi import APIRouter, Depends, Response
from fastapi_csrf_protect import CsrfProtect
from src.core.security import get_csrf_config

csrf_router = APIRouter()


@csrf_router.get('/form', tags=["csrf"])
def form(csrf_protect: CsrfProtect = Depends(get_csrf_config)):
    """
    Returns form template.

    :param csrf_protect:
    :return: form with csrf token in cookie
    """
    response = Response()
    csrf_protect.set_csrf_cookie(response)
    return response
