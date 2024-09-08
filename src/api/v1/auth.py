from datetime import datetime

from fastapi import APIRouter, Response, status

from api.depends import DatabaseType
from schemas.token import Token
from schemas.auth import UserSignIn, UserSignUp
from services.auth import auth_service
from utils.constants import COOKIE_AUTH_PATH

auth_router = APIRouter()


def set_auth_cookie(response: Response,
                    token: Token,
                    jwt_expires: datetime) -> Response:
    response.set_cookie(COOKIE_AUTH_PATH,
                        f'Bearer {token.access_token}',
                        expires=jwt_expires,
                        httponly=True)
    return response


@auth_router.post('/register',
                  status_code=status.HTTP_201_CREATED,
                  response_model=Token)
async def sign_up(response: Response, user: UserSignUp, db: DatabaseType):
    access_token, jwt_expires = await auth_service.signup(db, user=user)
    set_auth_cookie(response, access_token, jwt_expires)
    return access_token


@auth_router.post('/auth',
                  status_code=status.HTTP_200_OK,
                  response_model=Token)
async def sign_in(response: Response, user: UserSignIn, db: DatabaseType):
    access_token, jwt_expires = await auth_service.signin(db, user=user)
    set_auth_cookie(response, access_token, jwt_expires)
    return access_token
