from collections.abc import Awaitable, Callable

from jwt import decode as jwt_decode
from fastapi import Request, Response

from core import app_settings
from utils.constants import COOKIE_AUTH_PATH, SCOPE_AUTH_PATH, SCOPE_USER_PATH


async def bearer_authorization(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request.scope[SCOPE_AUTH_PATH] = False
    request.scope[SCOPE_USER_PATH] = None

    if COOKIE_AUTH_PATH in request.cookies:
        authorization_cookie = request.cookies[COOKIE_AUTH_PATH]
        access_token = authorization_cookie.removeprefix('Bearer ')
        try:
            jwt_data = jwt_decode(access_token,
                                  app_settings.secret_key,
                                  [app_settings.jwt_algorithm])
        except Exception:
            pass
        else:
            request.scope[SCOPE_AUTH_PATH] = True
            request.scope[SCOPE_USER_PATH] = jwt_data['sub']

    return await call_next(request)
