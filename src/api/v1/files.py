from typing import Annotated

from fastapi import APIRouter, File, Form, Query, UploadFile, status
from fastapi.responses import RedirectResponse

from api.depends import UserType, DatabaseType
from schemas.file import File as FileSchema, UserFiles
from services.file import file_crud
from utils.constants import FILE_PATH_MAX_LENGTH, FILE_PATH_MIN_LENGTH

files_router = APIRouter()

FormPathType = Annotated[str, Form(min_length=FILE_PATH_MIN_LENGTH,
                                   max_length=FILE_PATH_MAX_LENGTH)]

QueryPathOrIdType = Annotated[str, Query(alias='path',
                                         min_length=FILE_PATH_MIN_LENGTH,
                                         max_length=FILE_PATH_MAX_LENGTH)]


@files_router.get('',
                  status_code=status.HTTP_200_OK,
                  response_model=UserFiles)
async def user_files(user: UserType):
    return await file_crud.user_files(user=user)


@files_router.post('/upload',
                   status_code=status.HTTP_201_CREATED,
                   response_model=FileSchema)
async def upload_file(path: FormPathType,
                      file: Annotated[UploadFile, File()],
                      user: UserType,
                      db: DatabaseType):
    return await file_crud.upload(db, raw_path=path, file=file, user=user)


@files_router.get('/download', response_class=RedirectResponse)
async def download_file(path_or_id: QueryPathOrIdType,
                        user: UserType,
                        db: DatabaseType):

    return RedirectResponse(
        url=await file_crud.download(db, path_or_id=path_or_id, user=user),
        status_code=status.HTTP_302_FOUND)
