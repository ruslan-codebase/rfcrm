from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel


class Database(ABC):
    def __init__(self):
        self.async_engine: Optional[AsyncEngine] = None
        self.async_sessionmaker: Optional[sessionmaker] = None
        self.setup()

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        if self.async_sessionmaker is None:
            raise ValueError("async_sessionmaker not available. run setup() first")

        async with self.async_sessionmaker() as session:
            yield session

    async def init_db(self) -> None:
        if self.async_engine is None:
            raise ValueError("async_engine not available. run setup() first")

        async with self.async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def destroy_db(self) -> None:
        if self.async_engine is None:
            raise ValueError("async_engine not available. run setup() first")

        async with self.async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    @abstractmethod
    def setup(self) -> None:
        pass
