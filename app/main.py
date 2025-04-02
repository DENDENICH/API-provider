from pathlib import Path
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import yaml

from core import settings
from core.db import db_core
from api import router


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
    openapi_url="/openapi/orders.json",
    docs_url="/docs/orders",
    lifespan=lifespan,
    default_response_class=ORJSONResponse
)
app_main.include_router(router, prefix=settings.api.prefix)


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
        log_level="info"  # Adjust log level as needed
    )
