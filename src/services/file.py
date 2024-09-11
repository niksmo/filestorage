from pathlib import Path
from typing import Any, Type
from urllib.parse import urljoin

from fastapi import UploadFile, status
from fastapi.exceptions import HTTPException
from aiofiles import open as aiofiles_open
from aiofiles.os import makedirs as aiofiles_makedirs
from aiofiles.ospath import exists as aiofiles_exists
from sqlalchemy.ext.asyncio import AsyncSession

from core import app_settings
from models.file import File as FileModel
from schemas.file import File, FileCreate, UserFiles
from schemas.user import UserDB
from utils.constants import CHUNK_1MB
from .base import RepositoryDB


class RepositoryFile(RepositoryDB[FileModel, FileCreate, Any]):

    def __init__(self, model: Type[FileModel]) -> None:
        super().__init__(model)

    def _get_path_and_filename(self,
                               raw_path: str,
                               file: UploadFile) -> tuple[str, Path]:
        path = Path(raw_path)
        if path.is_absolute():
            path = Path(str(path)[1:])
        filename = raw_path.rsplit('/', maxsplit=1)[-1]
        if not filename:
            filename = file.filename if file.filename else 'file'
            path = path / filename
        return filename, path

    def _get_upload_path(self, path: Path, user: UserDB) -> Path:
        return app_settings.media_root.joinpath(user.media_id, path)

    async def _create_dirs(self, upload_path: Path) -> None:
        path_dir = upload_path.parent
        await aiofiles_makedirs(str(path_dir), exist_ok=True)

    async def user_files(self, db: AsyncSession, *,
                         user: UserDB) -> UserFiles:
        results = await self.get_multi(db, user_id=user.id)
        files = [File.model_validate(result) for result in results]
        return UserFiles(account_id=user.id, files=files)

    async def upload(self, db: AsyncSession, *,
                     raw_path: str,
                     file: UploadFile,
                     user: UserDB) -> FileModel:
        filename, path = self._get_path_and_filename(raw_path, file)
        upload_path = self._get_upload_path(path, user)

        if await aiofiles_exists(upload_path):
            raise HTTPException(status.HTTP_409_CONFLICT)

        await self._create_dirs(upload_path)

        try:
            async with aiofiles_open(upload_path, 'wb') as file_in_media:
                while data := await file.read(CHUNK_1MB):
                    await file_in_media.write(data)
        except Exception:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE)
        finally:
            await file.close()

        file_url = urljoin(app_settings.media_url, str(
            upload_path.relative_to(app_settings.media_root)))

        return await self.create(
            db,
            obj_in=FileCreate(path=f'/{str(path)}',
                              url=file_url,
                              name=filename,
                              size=file.size if file.size else 0,
                              user_id=user.id)
        )

    async def download(self, db: AsyncSession, *,
                       path_or_id: str,
                       user: UserDB) -> str:
        path = Path(path_or_id)
        if not path.is_absolute():
            path = f'/{path}'
        else:
            path = str(path)

        file_obj = await self.get(db, path=path, user_id=user.id)

        if not file_obj and path_or_id.isnumeric():
            file_obj = await self.get(db, id=int(path_or_id), user_id=user.id)

        if not file_obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        return file_obj.url


file_crud = RepositoryFile(FileModel)
