from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import UUID


class CRUDService(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def get(self, offset: int = 0, limit: int = 20):
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID):
        pass

    @abstractmethod
    async def create(self, model_in):
        pass

    @abstractmethod
    async def delete(self, id: UUID):
        pass

    @abstractmethod
    async def update(self, id: UUID, model_in):
        pass
