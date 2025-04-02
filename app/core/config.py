from pathlib import Path
from pydantic import BaseModel, PostgresDsn, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class ApiUsersPrefix(BaseModel):
    prefix: str = "/users"
    tags: list[str] = ["Users"]

class ApiSuppliesPrefix(BaseModel):
    prefix: str = "/supplies"
    tags: list[str] = ["Supplies"]

class ApiProductsPrefix(BaseModel):
    prefix: str = "/products"
    tags: list[str] = ["Products"]

class ApiAuthPrefix(BaseModel):
    prefix: str = "/auth"
    tags: list[str] = ["Auth"]

class ApiOrganizerPrefix(BaseModel):
    prefix: str = "/organizers"
    tags: list[str] = ["Organizers"]

class ApiExpensePrefix(BaseModel):
    prefix: str = "/expenses"
    tags: list[str] = ["Expenses"]

class ApiSupplierPrefix(BaseModel):
    prefix: str = "/suppliers"
    tags: list[str] = ["Suppliers"]

class ApiSetting(BaseModel):
    prefix: str = "/rosso"
    users: ApiUsersPrefix = ApiUsersPrefix()
    organizers: ApiOrganizerPrefix = ApiOrganizerPrefix()
    expenses: ApiExpensePrefix = ApiExpensePrefix()
    supplies: ApiSuppliesPrefix = ApiSuppliesPrefix()
    products: ApiProductsPrefix = ApiProductsPrefix()
    auth: ApiAuthPrefix = ApiAuthPrefix()
    suppliers: ApiSupplierPrefix = ApiSupplierPrefix()


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 7654


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
        env_file=(
            BASE_DIR / ".env.template",
            BASE_DIR / ".env"
        ),
        case_sensitive=False,
        env_nested_delimiter="__", # делители в .env файле между классами и полями
        env_prefix="APP_CONFIG__" # начальный префих
    )
    run: RunConfig = RunConfig()
    api: ApiSetting = ApiSetting()
    database: DataBaseConfig


settings = Settings()
