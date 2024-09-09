from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from utils.constants import FILE_NAME_MAX_LENGTH, FILE_PATH_MAX_LENGTH


class File(Base):

    __tablename__ = 'file'

    name: Mapped[str] = mapped_column(String(FILE_NAME_MAX_LENGTH))
    path: Mapped[str] = mapped_column(
        String(FILE_PATH_MAX_LENGTH), unique=True
    )
    url: Mapped[str] = mapped_column()
    size: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE')
    )
    user = relationship('User', back_populates='files')

    def __repr__(self):
        return f'File(id={self.id}, user_id={self.user_id}, path={self.path})'
