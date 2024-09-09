from typing import Annotated

from fastapi import APIRouter, File, Form, Query, UploadFile, status

from api.depends import UserIdType, DatabaseType
from schemas.file import File as FileSchema, UserFiles
from services.file import file_crud
from utils.constants import FILE_PATH_MAX_LENGTH, FILE_PATH_MIN_LENGTH

files_router = APIRouter()

FormPathType = Annotated[str, Form(min_length=FILE_PATH_MIN_LENGTH,
                                   max_length=FILE_PATH_MAX_LENGTH)]

QueryPathType = Annotated[str, Query(min_length=FILE_PATH_MIN_LENGTH,
                                     max_length=FILE_PATH_MAX_LENGTH)]


@files_router.get('',
                  status_code=status.HTTP_200_OK,
                  response_model=UserFiles)
async def user_files(user_id: UserIdType, db: DatabaseType):
    return await file_crud.user_files(db, user_id=user_id)


@files_router.post('/upload',
                   status_code=status.HTTP_201_CREATED,
                   response_model=FileSchema)
async def upload_file(path: FormPathType,
                      file: Annotated[UploadFile, File()],
                      user_id: UserIdType,
                      db: DatabaseType):
    return await file_crud.upload(
        db,
        raw_path=path,
        file=file,
        user_id=user_id
    )


@files_router.get('/download')
async def download_file(path: QueryPathType,
                        user_id: UserIdType):
    breakpoint()
    # path is str but may be ID
    # check owner in service
    # get static path
    return {'path': path}
