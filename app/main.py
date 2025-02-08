import uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run(
        app="main:app",
        reload=True,
        host="0.0.0.0",
        port=8000,
        log_level="info"  # Adjust log level as needed
    )
