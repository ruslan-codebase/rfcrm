from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.base_database import Database


class InMemSqliteDatabase(Database):
    def setup(self) -> None:
        sqliteurl = "sqlite+aiosqlite://"
        self.async_engine = create_async_engine(sqliteurl)
        self.async_sessionmaker = sessionmaker(
            bind=self.async_engine, class_=AsyncSession, expire_on_commit=False
        )
