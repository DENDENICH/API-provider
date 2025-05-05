from pathlib import Path
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
import yaml

from core import settings
from core.db import db_core

from api import router as api_router
from auth import router as auth_router

from pathlib import Path

import yaml
from fastapi import FastAPI
from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)
from starlette import status
from starlette.middleware.base import (
    RequestResponseEndpoint,
    BaseHTTPMiddleware,
)
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from auth.utils.jwt_processes import jwt_processes as jwt
# системные параметры

# Включение/выключение аутентификации. Используется False при дебаге
AUTH_ON = True  


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    await db_core.dispose()


class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # if os.getenv("AUTH_ON", "False") != "True":
        #     request.state.user_id = "test"
        #     return await call_next(request)

        if not AUTH_ON:
            request.state.user_id = "test"
            return await call_next(request) 

        elif request.url.path in [
            "/docs", 
            "/openapi/rosso.json",
            f"{settings.api.auth.prefix}/register",
            f"{settings.api.auth.prefix}/login"
        ]:
            return await call_next(request)
        
        elif request.method == "OPTIONS":
            return await call_next(request)

        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Missing access token",
                    "body": "Missing access token",
                },
            )
        try:
            auth_token = bearer_token.split(" ")[1].strip()
            token_payload = jwt.decode_jwt(auth_token)
        except (
            ExpiredSignatureError,
            ImmatureSignatureError,
            InvalidAlgorithmError,
            InvalidAudienceError,
            InvalidKeyError,
            InvalidSignatureError,
            InvalidTokenError,
            MissingRequiredClaimError,
        ) as error:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": str(error), "body": str(error)},
            )
        except Exception as error:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token", "body": "Invalid token"},
            )
        else:
            request.state.user_id = int(token_payload["sub"])
        return await call_next(request)
    

app_main = FastAPI(
    title="ROSSO API",
    debug=True,
    openapi_url="/openapi/rosso.json",
    docs_url="/docs",
    lifespan=lifespan,
)

# регистрация роутеров
app_main.include_router(api_router)
app_main.include_router(auth_router)

# регистрация middlewares
app_main.add_middleware(AuthorizeRequestMiddleware)
# TODO: донастроить параметры CORS
app_main.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавление собственной документации openapi в swagger
openapi_doc = yaml.safe_load(
    (Path(__file__).parent / "api" / "openapi" / "openapi.yaml").read_text()
)

app_main.openapi = lambda: openapi_doc


if __name__ == '__main__':
    uvicorn.run(
        app="main:app_main",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
        log_level="info" 
    )
