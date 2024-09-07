from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import async_session


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session.begin() as session:
        yield session

DatabaseType = Annotated[AsyncSession, Depends(get_session)]
