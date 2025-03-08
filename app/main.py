from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

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
    lifespan=lifespan,
    default_response_class=ORJSONResponse
)
app_main.include_router(router, prefix=settings.api.prefix)


if __name__ == '__main__':
    uvicorn.run(
        app="main:app_main",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
        log_level="info"  # Adjust log level as needed
    )
