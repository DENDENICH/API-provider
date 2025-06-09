from pathlib import Path
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
CORE_DIR = Path(__file__).resolve().parent


class ApiUsersPrefix:
    prefix: str = "/users"
    tags: list[str] = ["Users"]

class ApiSuppliesPrefix:
    prefix: str = "/supplies"
    tags: list[str] = ["Supplies"]

class ApiProductsPrefix:
    prefix: str = "/products"
    tags: list[str] = ["Products"]

class ApiAuthPrefix:
    prefix: str = "/auth"
    tags: list[str] = ["Auth"]

class ApiOrganizersPrefix:
    prefix: str = "/organizers"
    tags: list[str] = ["Organizers"]

class ApiExpensesPrefix:
    prefix: str = "/expenses"
    tags: list[str] = ["Expenses"]

class ApiSuppliersPrefix:
    prefix: str = "/suppliers"
    tags: list[str] = ["Suppliers"]

class ApiLinkCodePrefix:
    prefix: str = "/linkcode"
    tags: list[str] = ["LinkCode"]

class ApiDashboardPrefix:
    prefix: str = "/dashboard"
    tags: list[str] = ["Dashboard"]

class ApiSetting:
    users: ApiUsersPrefix = ApiUsersPrefix()
    organizers: ApiOrganizersPrefix = ApiOrganizersPrefix()
    expenses: ApiExpensesPrefix = ApiExpensesPrefix()
    supplies: ApiSuppliesPrefix = ApiSuppliesPrefix()
    products: ApiProductsPrefix = ApiProductsPrefix()
    auth: ApiAuthPrefix = ApiAuthPrefix()
    suppliers: ApiSuppliersPrefix = ApiSuppliersPrefix()
    linkcode: ApiLinkCodePrefix = ApiLinkCodePrefix()
    dashboard: ApiDashboardPrefix = ApiDashboardPrefix()


class AuthSettings(BaseSettings):
    private_key: Path = CORE_DIR / 'certs' / 'private.pem'
    public_key: Path = CORE_DIR / 'certs' / 'public.pem'
    algorithm: str = 'RS256'
    access_token_expire_hours: int = 12


class RunConfig:
    """Класс настроек сервера"""
    host: str = "localhost"
    port: int = 7654


class DataBaseConfig(BaseModel):
    """Класс настроек БД"""
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
    auth: AuthSettings = AuthSettings()


settings = Settings()
