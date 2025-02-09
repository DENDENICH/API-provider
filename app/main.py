from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from config import config
from db import db_core
from api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    await db_core.dispose()

app_main = FastAPI(
    lifespan=lifespan
)
app_main.include_router(router, prefix=config.api.prefix)


if __name__ == '__main__':
    uvicorn.run(
        app="main:app_main",
        reload=True,
        host=config.run.host,
        port=config.run.port,
        log_level="info"  # Adjust log level as needed
    )
