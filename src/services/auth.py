from datetime import datetime, timedelta, timezone
from typing import Any, Protocol, runtime_checkable

from argon2 import PasswordHasher
from jwt import encode as jwt_encode
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import app_settings
from schemas.auth import UserSignIn, UserSignUp
from schemas.token import Token
from services.user import RepositoryUser, crud_user


@runtime_checkable
class SupportsPasswordHasher(Protocol):
    def hash(self, password: str) -> str:
        ...

    def verify(self, hash: str, password: str) -> Any:
        ...

    def check_needs_rehash(self, hash: str) -> bool:
        ...


class AuthService:
    def __init__(self,
                 crud_user: RepositoryUser,
                 pwd_hasher: SupportsPasswordHasher) -> None:
        self._crud_user = crud_user
        self._pwd_hasher = pwd_hasher

    def _create_access_token(
        self,
        sub_id: int,
        expires_delta: timedelta
    ) -> tuple[Token, datetime]:
        exp_datetime = datetime.now(timezone.utc) + expires_delta
        return (Token(
            access_token=jwt_encode(
                {'sub': sub_id, 'exp': exp_datetime},
                app_settings.secret_key,
                app_settings.jwt_algorithm
            ),
            token_type='bearer'
        ), exp_datetime)

    async def signup(self, db: AsyncSession, *,
                     user: UserSignUp) -> tuple[Token, datetime]:
        existed = await self._crud_user.get(db, username=user.username)
        if existed:
            raise HTTPException(status.HTTP_409_CONFLICT)
        user.password = self._pwd_hasher.hash(user.password)
        user_instance = await self._crud_user.create(db, obj_in=user)

        return self._create_access_token(
            user_instance.id,
            timedelta(seconds=app_settings.jwt_expires)
        )

    async def signin(self, db: AsyncSession, *,
                     user: UserSignIn) -> tuple[Token, datetime]:
        user_instance = await self._crud_user.get(db, username=user.username)
        if not user_instance:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)

        try:
            self._pwd_hasher.verify(user_instance.password, user.password)
        except Exception:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)

        if self._pwd_hasher.check_needs_rehash(user_instance.password):
            await self._crud_user.update(
                db,
                id=user_instance.id,
                password=self._pwd_hasher.hash(user.password)
            )
        return self._create_access_token(
            user_instance.id,
            timedelta(seconds=app_settings.jwt_expires)
        )


auth_service = AuthService(crud_user, PasswordHasher())
