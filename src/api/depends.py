from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from jwt import decode as jwt_decode
from sqlalchemy.ext.asyncio import AsyncSession

from core import app_settings
from db import async_session
from utils.constants import COOKIE_AUTH_PATH


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session.begin() as session:
        yield session


async def get_auth_user_id(request: Request) -> int:
    if COOKIE_AUTH_PATH not in request.cookies:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        jwt_data = jwt_decode(
            request.cookies[COOKIE_AUTH_PATH].removeprefix('Bearer '),
            app_settings.secret_key,
            [app_settings.jwt_algorithm]
        )
    except Exception:
        HTTPException(status.HTTP_401_UNAUTHORIZED)

    return jwt_data['sub']


DatabaseType = Annotated[AsyncSession, Depends(get_session)]
AuthUserIdType = Annotated[int, Depends(get_auth_user_id)]
