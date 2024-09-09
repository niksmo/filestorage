from datetime import datetime
from collections.abc import Sequence

from pydantic import BaseModel as BaseSchema, Field

from utils.constants import FILE_PATH_MAX_LENGTH, FILE_PATH_MIN_LENGTH

__all__ = ('FileUpload', 'FileCreate', 'File', 'UserFiles')


class FileBase(BaseSchema):
    path: str = Field(max_length=FILE_PATH_MAX_LENGTH,
                      min_length=FILE_PATH_MIN_LENGTH)


class FileUpload(FileBase):
    pass


class FileCreate(FileBase):
    name: str
    size: int
    user_id: int


class File(FileBase):
    id: int
    name: str
    size: int
    created_at: datetime
    active: bool

    model_config = {'from_attributes': True}


class UserFiles(BaseSchema):
    account_id: int
    files: list[File]
