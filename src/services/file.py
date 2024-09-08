from typing import Any

from models.file import File as FileModel
from schemas.file import FileCreate as FileCreateSchema
from .base import RepositoryDB


class RepositoryFile(RepositoryDB[FileModel, FileCreateSchema, Any]):
    pass


file_crud = RepositoryFile(FileModel)
