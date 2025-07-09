from typing import Awaitable, Callable

from core import settings
from core.db import db_core

from jwt import ExpiredSignatureError

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from auth.utils.jwt_processes import jwt_processes as _jwt

# Включение/выключение аутентификации. Используется False при дебаге
AUTH_ON = True


UNAUTHENTICATED_ONLY_PATHS: set[str] = {
    f"{settings.api.auth.prefix}/register",
    f"{settings.api.auth.prefix}/login"
}

PUBLIC_PATHS: set[str] = {
    "/docs",
    "/openapi/rosso.json",
    "/redoc"
}


class FullAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self,
            request: Request,
            call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:

        path = request.url.path
        new_access_token = False

        if not AUTH_ON:
            request.state.user_id = "test"
            return await call_next(request)

        elif path in PUBLIC_PATHS:
            return await call_next(request)

        elif request.method == "OPTIONS":
            return await call_next(request)

        access_token = request.cookies.get('Bearer-token')
        refresh_token = request.cookies.get('Refresh-token')

        if not access_token and refresh_token:
            user_id = int(_jwt.decode_jwt(refresh_token).get('sub'))
            access_token = _jwt.create_access_token(user_id)
            new_access_token = True

        current_user_id = None
        try:
            current_user_id = _jwt.decode_jwt(access_token).get('sub')
        except ExpiredSignatureError as e:
            current_user_id = _jwt.decode_jwt(refresh_token).get('sub')
            new_access_token = True

        # get db session
        request.state.session = db_core.get_session()

        # current_user = await UserService().get_by_id(uow, current_user_id) # can be used for request.state.current_user
        if not current_user_id:  # before current_user
            if path in UNAUTHENTICATED_ONLY_PATHS:
                response = await call_next(request)
                refresh_token = _jwt.create_refresh_token(request.state.user_id)
                access_token = _jwt.create_access_token(request.state.user_id)
                response.set_cookie('Refresh-token', refresh_token)
                response.set_cookie('Bearer-token', access_token)
                return response
            else:
                # raise UnauthenticatedError
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": 'Unauthenticated'}
                )

        if path in UNAUTHENTICATED_ONLY_PATHS:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "This path is only for unauthenticated users"}
            )

        elif path not in UNAUTHENTICATED_ONLY_PATHS and path not in PUBLIC_PATHS:
            if path == "/auth/logout":
                response = await call_next(request)
                response.delete_cookie('Bearer-token')
                response.delete_cookie('Refresh-token')
                return response

            request.state.user_id = current_user_id
            response = await call_next(request)
            if new_access_token:
                response.set_cookie('Bearer-token', access_token)
            return response

        else:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Forbidden"}
            )
