import contextlib
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


class DBSessionManager:
    def __init__(self, **kwargs: Any):
        self._engine = create_async_engine(settings.DATABASE_URL,
                                           future=True,
                                           echo=settings.DEBUG,
                                           pool_pre_ping=True,
                                           **kwargs)
        self._session_maker = async_sessionmaker(bind=self._engine,
                                                 expire_on_commit=False,
                                                 autoflush=False,
                                                 class_=AsyncSession)

    @property
    def engine(self):
        return self._engine

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self._session_maker:
            raise ValueError("DB Session maker is not initialized")

        async with self._session_maker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    @contextlib.asynccontextmanager
    async def connection(self) -> AsyncGenerator[AsyncConnection, None]:
        if not self._engine:
            raise ValueError("DB Engine is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception as e:
                await connection.rollback()
                raise e

    async def close(self):
        if not self._engine:
            raise ValueError("DB Engine is not initialized")

        await self._engine.dispose()
        self._engine = None
        self._session_maker = None


session_manager = DBSessionManager()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.session() as session:
        yield session
