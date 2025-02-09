from pydantic import BaseModel, PostgresDsn, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 7654


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int


class Settings(BaseSettings):
    # параметр для подключения базы данных и чтения параметров из env файла
    model_config = SettingsConfigDict(
        env_file=("app/.env.template", "app/.env"),
        case_sensitive=False,
        env_nested_delimiter="__", # делители в .env файле между классами и полями
        env_prefix="APP_CONFIG__" # начальный префих
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    database: DataBaseConfig


try:
    settings = Settings()
except ValidationError as e:
    print(e)
