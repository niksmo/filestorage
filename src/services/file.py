from pathlib import Path
from typing import Any

from fastapi import UploadFile, status
from fastapi.exceptions import HTTPException
from aiofiles import open as aiofiles_open
from aiofiles.os import makedirs as aiofiles_makedirs
from aiofiles.ospath import exists as aiofiles_exists
from sqlalchemy.ext.asyncio import AsyncSession

from core import app_settings
from models.file import File as FileModel
from schemas.file import File, FileCreate, UserFiles
from utils.constants import CHUNK_1MB
from .base import RepositoryDB


class RepositoryFile(RepositoryDB[FileModel, FileCreate, Any]):

    def _get_path_and_filename(self,
                               raw_path: str,
                               file: UploadFile) -> tuple[str, Path]:
        path = Path(f'/{raw_path}')
        filename = raw_path.rsplit('/', maxsplit=1)[-1]
        if not filename:
            filename = file.filename if file.filename else 'file'
            path = path.with_name(filename)
        return filename, path

    def _get_upload_path(self, path: Path, user_id: int) -> Path:
        return app_settings.media_root.joinpath(str(user_id),
                                                str(path).removeprefix('/'))

    async def _create_dirs(self, upload_path: Path) -> None:
        path_dir = upload_path.parent
        await aiofiles_makedirs(str(path_dir), exist_ok=True)

    async def user_files(self, db: AsyncSession, *,
                         user_id: int) -> UserFiles:
        objects = await self.get_multi(db, user_id=user_id)
        files = [File.model_validate(file_obj) for file_obj in objects]
        return UserFiles(account_id=user_id, files=files)

    async def upload(self, db: AsyncSession, *,
                     raw_path: str,
                     file: UploadFile,
                     user_id: int) -> FileModel:
        filename, path = self._get_path_and_filename(raw_path, file)
        upload_path = self._get_upload_path(path, user_id)

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

        return await self.create(
            db,
            obj_in=FileCreate(path=str(path),
                              name=filename,
                              size=file.size if file.size else 0,
                              user_id=user_id)
        )

    async def download(self, db: AsyncSession, *, foo):
        pass


file_crud = RepositoryFile(FileModel)
