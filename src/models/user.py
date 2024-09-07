import re

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from models.base import Base
from utils.constants import (PASSWORD_MAX_LENGTH, USERNAME_MAX_LENGTH,
                             USERNAME_PATTERN)

username_re = re.compile(USERNAME_PATTERN)


class User(Base):

    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(String(USERNAME_MAX_LENGTH),
                                          unique=True)
    password: Mapped[str] = mapped_column(String(PASSWORD_MAX_LENGTH))
    active: Mapped[bool] = mapped_column(default=True)
    # files = relationship('File', back_populates='user')

    @validates('username')
    def validate_username(self, _, username):
        if not username_re.match(username):
            raise ValueError('Enter a valid “username” consisting of letters, '
                             'numbers, underscores or hyphens.')
        return username

    def __repr__(self):
        return ('User(\n'
                f'  id={self.id},\n'
                f'  username={self.username},\n'
                ')')
