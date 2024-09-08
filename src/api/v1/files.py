from typing import Annotated

from fastapi import APIRouter, File, Form, Query, UploadFile, status

from api.depends import UserIdType
from schemas.file import File as FileSchema
from utils.constants import FILE_PATH_MAX_LENGTH, FILE_PATH_MIN_LENGTH

files_router = APIRouter()

FromPathType = Annotated[str, Form(min_length=FILE_PATH_MIN_LENGTH,
                                   max_length=FILE_PATH_MAX_LENGTH)]

QueryPathType = Annotated[str, Query(min_length=FILE_PATH_MIN_LENGTH,
                                     max_length=FILE_PATH_MAX_LENGTH)]


@files_router.get('')
async def user_files():
    pass


@files_router.post('/upload',
                   status_code=status.HTTP_201_CREATED,
                   response_model=FileSchema)
async def upload_file(path: FromPathType,
                      file: Annotated[UploadFile, File()],
                      user_id: UserIdType):
    breakpoint()
    # in service make correct path if it folder
    return {'path': path}


@files_router.get('/download')
async def download_file(path: QueryPathType,
                        user_id: UserIdType):
    breakpoint()
    # path is str but may be ID
    # check owner in service
    # get static path
    # regirect to nginx?
    return {'path': path}
