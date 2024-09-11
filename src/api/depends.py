from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import async_session
from schemas.user import UserDB


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session.begin() as session:
        yield session


def verify_auth(request: Request) -> UserDB:
    if not request.auth:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return request.user


UserType = Annotated[UserDB, Depends(verify_auth)]
DatabaseType = Annotated[AsyncSession, Depends(get_session)]
