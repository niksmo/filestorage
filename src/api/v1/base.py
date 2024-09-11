from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import ScalarResult, text
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends import get_session
from schemas.healthcheck import ServiceActiveTime
from utils.constants import TAG_AUTH, TAG_FILES, TAG_HEALTHCHECK, UNAVAILABLE
from utils.make import make_json_response_example

from .auth import auth_router
from .files import files_router

router_v1 = APIRouter()
router_v1.include_router(auth_router, prefix='', tags=[TAG_AUTH])
router_v1.include_router(files_router, prefix='/files', tags=[TAG_FILES])

DatabaseType = Annotated[AsyncSession, Depends(get_session)]


@router_v1.get('/ping',
               response_model=ServiceActiveTime,
               status_code=status.HTTP_200_OK,
               responses={
                   status.HTTP_503_SERVICE_UNAVAILABLE:
                   make_json_response_example(
                       example=ServiceActiveTime(
                           db=UNAVAILABLE, cache=UNAVAILABLE).model_dump()
                   )
               },
               tags=[TAG_HEALTHCHECK])
async def service_active_time(db: DatabaseType):
    try:
        result: ScalarResult[timedelta] = await db.scalars(
            text('SELECT current_timestamp - pg_postmaster_start_time();')
        )
    except Exception:
        db_uptime = UNAVAILABLE
    else:
        db_uptime = int(result.one().total_seconds())

    redis_backend: RedisBackend = FastAPICache.get_backend()  # type: ignore
    try:
        info = await redis_backend.redis.info()  # type: ignore
    except Exception:
        cache_uptime = UNAVAILABLE
    else:
        cache_uptime = info["uptime_in_seconds"]

    return ServiceActiveTime(db=db_uptime, cache=cache_uptime)
