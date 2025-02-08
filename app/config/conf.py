from pydantic import BaseModel
from pydantic_settings import BaseSettings

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 7654


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class Config(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


config = Config()