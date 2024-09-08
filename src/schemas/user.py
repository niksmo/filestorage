from pydantic import BaseModel as BaseSchema, Field

from utils.constants import (PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH,
                             USERNAME_PATTERN, USERNAME_MAX_LENGTH,
                             USERNAME_MIN_LENGTH)


class UserBase(BaseSchema):
    username: str = Field(pattern=USERNAME_PATTERN,
                          min_length=USERNAME_MIN_LENGTH,
                          max_length=USERNAME_MAX_LENGTH)

    password: str = Field(min_length=PASSWORD_MIN_LENGTH,
                          max_length=PASSWORD_MAX_LENGTH)


class UserCreate(UserBase):
    pass
