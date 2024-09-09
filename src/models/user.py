import hmac
from hashlib import sha256
import re
from secrets import token_urlsafe

from sqlalchemy import String
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from core import app_settings
from models.base import Base
from utils.constants import (PASSWORD_MAX_LENGTH, USERNAME_MAX_LENGTH,
                             URL_MEDIA_TOKEN_BYTES, USERNAME_PATTERN,)

username_re = re.compile(USERNAME_PATTERN)


def make_media_id(context: DefaultExecutionContext) -> str:
    hashed_username = hmac.digest(
        app_settings.secret_key.encode(encoding='utf-8'),
        context.get_current_parameters()['username'].encode(encoding='utf-8'),
        sha256
    ).hex()
    return f'{hashed_username}{token_urlsafe(URL_MEDIA_TOKEN_BYTES)}'


class User(Base):

    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(String(USERNAME_MAX_LENGTH),
                                          unique=True)

    password: Mapped[str] = mapped_column(String(PASSWORD_MAX_LENGTH))

    media_id: Mapped[str] = mapped_column(default=make_media_id)

    files = relationship('File', back_populates='user',
                         collection_class=list, cascade='delete')

    @validates('username')
    def validate_username(self, _, username):
        if not username_re.match(username):
            raise ValueError('Enter a valid “username” consisting of letters, '
                             'numbers, underscores or hyphens.')
        return username

    def __repr__(self):
        return (f'User(id={self.id}, username={self.username}, '
                f'media_id={self.media_id})')
