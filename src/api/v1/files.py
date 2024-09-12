from typing import Annotated

from fastapi import APIRouter, File, Form, Query, UploadFile, status
from fastapi.responses import RedirectResponse
from fastapi_cache.decorator import cache

from api.depends import AuthUserIdType, DatabaseType
from schemas.file import File as FileSchema, UserFiles
from services.file import file_crud
from utils.constants import (CACHE_60_S, FILE_PATH_MAX_LENGTH,
                             FILE_PATH_MIN_LENGTH)

files_router = APIRouter()

FormPathType = Annotated[str, Form(min_length=FILE_PATH_MIN_LENGTH,
                                   max_length=FILE_PATH_MAX_LENGTH)]

QueryPathOrIdType = Annotated[str, Query(alias='path',
                                         min_length=FILE_PATH_MIN_LENGTH,
                                         max_length=FILE_PATH_MAX_LENGTH)]


@files_router.get('',
                  status_code=status.HTTP_200_OK,
                  response_model=UserFiles)
@cache(expire=CACHE_60_S)
async def user_files(user_id: AuthUserIdType, db: DatabaseType):
    return await file_crud.user_files(db, user_id=user_id)


@files_router.post('/upload',
                   status_code=status.HTTP_201_CREATED,
                   response_model=FileSchema)
async def upload_file(path: FormPathType,
                      file: Annotated[UploadFile, File()],
                      user_id: AuthUserIdType,
                      db: DatabaseType):
    return await file_crud.upload(db,
                                  raw_path=path,
                                  file=file,
                                  user_id=user_id)


@files_router.get('/download',
                  status_code=status.HTTP_302_FOUND,
                  response_class=RedirectResponse)
@cache(expire=CACHE_60_S)
async def download_file(path_or_id: QueryPathOrIdType,
                        user_id: AuthUserIdType,
                        db: DatabaseType):
    return RedirectResponse(
        url=await file_crud.download(
            db, path_or_id=path_or_id, user_id=user_id
        ),
        status_code=status.HTTP_302_FOUND
    )
