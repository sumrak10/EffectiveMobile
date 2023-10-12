from typing import Any
from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy import insert, select, update, delete, desc
from sqlalchemy.ext.asyncio import AsyncSession

from models import SpimexTradingResults
from schemas import SpimexTradingResultSchema


class AbstractRepository(ABC):
    @abstractmethod
    def add_one(self, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_all(self) -> list[BaseModel]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].get_schema() for row in res.all()]
        return res

    async def get_all_with_filters(self, **filter_by) -> list[BaseModel]:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = [row[0].get_schema() for row in res.all()]
        return res


class SpimexTradingResultsRepository(SQLAlchemyRepository):
    model = SpimexTradingResults
