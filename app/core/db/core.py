from typing import AsyncGenerator
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    async_scoped_session
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
        self.engine = create_async_engine(
            url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow
        )

        self.session_maker = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False, # сами следим за актуальностью данных, при обращении
        )

    # Оставляем callable объектом для возможности вызова через Dependes()
    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """Генерация сессии"""
        async with self.session_maker() as session:
            yield session

    @property
    async def get_async_session(self) -> AsyncSession:
        """Создание и возврат объекта асинхронной сессии"""
        session = async_scoped_session(self.session_maker, scopefunc=current_task)
        return session()

    async def dispose(self) -> None:
        """Выключение и закрытие конекта с БД"""
        await self.engine.dispose()


db_core = DBCore(
    url=str(settings.database.url),
    echo=settings.database.echo,
    echo_pool=settings.database.echo_pool,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
)
