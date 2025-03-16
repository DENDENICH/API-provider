from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from core import settings


class DBCore:
    """Класс для настройки ядра подключения к БД SQLAlchemy"""
    def __init__(
        self,
        url: str,
        echo: bool,
        echo_pool: bool,
        pool_size: int = 5,
        max_overflow: int = 10
    ):
        self._engine = create_async_engine(
            url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow
        )

        self._session_maker = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False, # сами следим за актуальностью данных, при обращении
        )

    @property
    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """Генерация сессии"""
        async with self._session_maker() as session:
            yield session

    @property
    async def dispose(self) -> None:
        """Выключение и закрытие конекта с БД"""
        await self._engine.dispose()



db_core = DBCore(
    url=str(settings.database.url),
    echo=settings.database.echo,
    echo_pool=settings.database.echo_pool,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
)
