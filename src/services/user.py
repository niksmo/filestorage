from typing import Any

from models.user import User as UserModel
from schemas.user import UserCreate
from .base import RepositoryDB

__all__ = ('crud_user',)


class RepositoryUser(RepositoryDB[UserModel, UserCreate, Any]):
    pass


crud_user = RepositoryUser(UserModel)
