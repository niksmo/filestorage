from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import ScalarResult, text
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends import get_session
from schemas.healthcheck import ServiceActiveTime
from utils.constants import TAG_AUTH, TAG_FILES, TAG_HEALTHCHECK
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
                       example=ServiceActiveTime(db=0).model_dump()
                   )
               },
               tags=[TAG_HEALTHCHECK])
async def service_active_time(db: DatabaseType):
    try:
        result: ScalarResult[timedelta] = await db.scalars(
            text('SELECT current_timestamp - pg_postmaster_start_time();')
        )
    except ConnectionError:
        db_uptime = 0.00
    else:
        db_uptime = result.one().total_seconds()
    return ServiceActiveTime(db=db_uptime)
