from collections.abc import Awaitable, Callable

from jwt import decode as jwt_decode
from fastapi import Request, Response, status
from fastapi.exceptions import HTTPException

from db import async_session
from core import app_settings
from services.user import crud_user
from utils.constants import COOKIE_AUTH_PATH, SCOPE_AUTH_PATH, SCOPE_USER_PATH


async def bearer_authorization(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    if COOKIE_AUTH_PATH not in request.cookies:
        request.scope[SCOPE_AUTH_PATH] = False
        request.scope[SCOPE_USER_PATH] = None
        return await call_next(request)

    authorization_cookie = request.cookies[COOKIE_AUTH_PATH]
    access_token = authorization_cookie.removeprefix('Bearer ')
    try:
        jwt_data = jwt_decode(access_token,
                              app_settings.secret_key,
                              [app_settings.jwt_algorithm])
    except Exception:
        pass
    async with async_session.begin() as db:
        user_obj = await crud_user.get(db, id=jwt_data['sub'])
        if not user_obj:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        request.scope[SCOPE_AUTH_PATH] = True
        request.scope[SCOPE_USER_PATH] = user_obj
        return await call_next(request)
