from datetime import datetime

from pydantic import BaseModel as BaseSchema, Field

from utils.constants import FILE_PATH_MAX_LENGTH, FILE_PATH_MIN_LENGTH


class FileBase(BaseSchema):
    path: str = Field(max_length=FILE_PATH_MAX_LENGTH,
                      min_length=FILE_PATH_MIN_LENGTH)


class FileCreate(FileBase):
    name: str
    size: int


class File(FileCreate):
    id: int
    created_at: datetime
    active: bool
