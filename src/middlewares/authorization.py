from collections.abc import Awaitable, Callable

from jwt import decode as jwt_decode
from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from db import async_session
from core import app_settings
from services.user import crud_user
from schemas.user import UserDB
from utils.constants import COOKIE_AUTH_PATH, SCOPE_AUTH_PATH, SCOPE_USER_PATH


async def get_user_by_jwt_data(db: AsyncSession, id: int) -> UserDB:
    return UserDB.model_validate(await crud_user.get(db, id=id))


async def bearer_authorization(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request.scope[SCOPE_AUTH_PATH] = False
    request.scope[SCOPE_USER_PATH] = None

    if COOKIE_AUTH_PATH in request.cookies:
        authorization_cookie = request.cookies[COOKIE_AUTH_PATH]
        access_token = authorization_cookie.removeprefix('Bearer ')
        try:
            jwt_data = jwt_decode(access_token,
                                  app_settings.secret_key,
                                  [app_settings.jwt_algorithm])
        except Exception:
            return await call_next(request)

        async with async_session.begin() as db:
            user = await get_user_by_jwt_data(db, jwt_data['sub'])
            if user:
                request.scope[SCOPE_AUTH_PATH] = True
                request.scope[SCOPE_USER_PATH] = user

    return await call_next(request)
