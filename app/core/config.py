from pydantic import BaseModel, PostgresDsn, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 7654


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"
    tags: list[str] = ["Users"]


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

    naming_conventions: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }


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
