from contextlib import asynccontextmanager
import uvicorn

from core import settings
from core.db import db_core

from api import router as api_router
from auth import router as auth_router

from pathlib import Path

import yaml
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from middlewares import AuthorizeRequestMiddleware


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
    openapi_url="/openapi/rosso.json",
    docs_url="/docs",
    lifespan=lifespan,
)

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
