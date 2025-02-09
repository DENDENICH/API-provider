from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from config import config


class DBCore:
    """Class for core db"""
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

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_maker() as session:
            yield session

    async def dispose(self) -> None:
        await self._engine.dispose()



db_core = DBCore(
    url=str(config.db.url),
    echo=config.db.echo,
    echo_pool=config.db.echo_pool,
    pool_size=config.db.pool_size,
    max_overflow=config.db.max_overflow,
)
