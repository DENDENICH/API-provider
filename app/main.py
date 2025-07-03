from contextlib import asynccontextmanager
import uvicorn

from core import settings
from core.db import db_core

from api import router as api_router
from auth import router as auth_router

from pathlib import Path

import yaml
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from starlette.middleware.cors import CORSMiddleware

from middlewares import AuthorizeRequestMiddleware

from utils.transaction_context import CtxException

from service.bussines_services.user import UserService

from exceptions import NotFoundError, not_found_error

from exception_handlers import error_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    await db_core.dispose()
    

app_main = FastAPI(
    title="ROSSO API",
    debug=True,
    # openapi_url="/openapi/rosso.json",
    docs_url="/docs",
    lifespan=lifespan,
)
# error_handlers(app=app_main)

# from exceptions import SomeError
# @app_main.exception_handler(SomeError)
# async def failed_token_refresh_handler(request: Request, exc: SomeError):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.detail}
#     )

# async def ctx_exception_handler(request: Request, exc: CtxException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.detail}
#     )

# app_main.add_exception_handler(CtxException, ctx_exception_handler)



# async def ntf_exception_handler(request: Request, exc: not_found_error):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.detail}
#     )

# app_main.add_exception_handler(not_found_error, ntf_exception_handler)

#запуск обработчиков ошибок
# error_handlers(app=app_main)

# регистрация роутеров
app_main.include_router(api_router)
app_main.include_router(auth_router)

# регистрация middlewares
app_main.add_middleware(AuthorizeRequestMiddleware)
# TODO: донастроить параметры CORS - добавить домен и порт фронтенд приложения
app_main.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавление собственной документации openapi в swagger
# openapi_doc = yaml.safe_load(
#     (Path(__file__).parent / "api" / "openapi" / "openapi.yaml").read_text(encoding="utf-8")
# )

# app_main.openapi = lambda: openapi_doc

if __name__ == '__main__':
    uvicorn.run(
        app="main:app_main",
        reload=True,
        host='localhost',
        port=8000,
        log_level="info" 
    )
