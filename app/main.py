import uvicorn
from fastapi import FastAPI

from config import config
from api import router

app = FastAPI()
app.include_router(router, prefix=config.api.prefix)


if __name__ == '__main__':
    uvicorn.run(
        app="main:app",
        reload=True,
        host=config.run.host,
        port=config.run.port,
        log_level="info"  # Adjust log level as needed
    )
