from datetime import datetime

from fastapi import APIRouter, Response, status

from api.depends import DatabaseType
from schemas.token import Token
from schemas.user import User, UserCreate
from services.auth import auth_crud

auth_router = APIRouter()


def set_auth_cookie(response: Response,
                    token: Token,
                    jwt_expires: datetime) -> Response:
    response.set_cookie('Authorization',
                        f'Bearer {token.access_token}',
                        expires=jwt_expires,
                        httponly=True)
    return response


@auth_router.post('/register',
                  status_code=status.HTTP_201_CREATED,
                  response_model=Token)
async def sign_up(response: Response, user: UserCreate, db: DatabaseType):
    access_token, jwt_expires = await auth_crud.signup(db, user=user)
    set_auth_cookie(response, access_token, jwt_expires)
    return access_token


@auth_router.post('/auth',
                  status_code=status.HTTP_200_OK,
                  response_model=Token)
async def sign_in(response: Response, user: User, db: DatabaseType):
    access_token, jwt_expires = await auth_crud.signin(db, user=user)
    set_auth_cookie(response, access_token, jwt_expires)
    return access_token
