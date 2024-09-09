from collections.abc import Sequence
from typing import Generic, NoReturn, Optional, Type, TypeVar

from pydantic import BaseModel as BaseSchema
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base as BaseModel

__all__ = ('RepositoryDB',)

ModelType = TypeVar('ModelType', bound=BaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseSchema)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseSchema)


class RepositoryBase:
    def get(self, *args, **kwargs) -> NoReturn:
        raise NotImplementedError

    def get_multi(self, *args, **kwargs) -> NoReturn:
        raise NotImplementedError

    def create(self, *args, **kwargs) -> NoReturn:
        raise NotImplementedError

    def update(self, *args, **kwargs) -> NoReturn:
        raise NotImplementedError

    def delete(self, *args, **kwargs) -> NoReturn:
        raise NotImplementedError


class RepositoryDB(
    RepositoryBase,
    Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def get(self, db: AsyncSession,
                  **kwargs) -> Optional[ModelType]:
        stmt = select(self._model).filter_by(**kwargs)
        return await db.scalar(stmt)

    async def get_multi(self, db: AsyncSession,
                        **kwargs) -> Sequence[ModelType]:
        stmt = select(self._model).filter_by(**kwargs)
        return (await db.scalars(stmt)).all()

    async def create(self, db: AsyncSession, *,
                     obj_in: CreateSchemaType) -> ModelType:
        obj = self._model(**obj_in.model_dump())
        db.add(obj)
        await db.commit()
        return obj

    async def update(self, db: AsyncSession, *,
                     id: int, **kwargs) -> ModelType:
        result = await db.scalars(update(self._model).where(
            self._model.id == id).values(**kwargs).returning(self._model)
        )
        return result.one()
