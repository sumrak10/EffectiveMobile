import asyncio
import datetime

from services import TradingResultsService
from database import Base, engine


async def main():
    await create_tables()
    await TradingResultsService.download_for_period(
        period_end=datetime.date(2023, 1, 1)
    )


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(main())
