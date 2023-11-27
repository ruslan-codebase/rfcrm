from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.base_database import Database
from app.settings import settings


class PostgresDatabase(Database):

    def setup(self) -> None:
        self.async_engine = create_async_engine(
            settings.postgres_dsn,
            echo=True
        )
        self.async_sessionmaker = sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
