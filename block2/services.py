import datetime

from unitofwork import IUnitOfWork, UnitOfWork
from bs4_parser import get_links_for_period
from excel_parser import parse_all_data


class TradingResultsService:
    @classmethod
    async def download_for_period(cls,
                                  period_end: datetime.date,
                                  period_start: datetime.date | None = None,
                                  uow: IUnitOfWork = UnitOfWork()
                                  ):
        if period_start is None:
            period_start = datetime.datetime.now().date()
        links = await get_links_for_period(start_date=period_start, end_date=period_end)
        schemas = await parse_all_data(links)
        async with uow:
            for schema in schemas:
                await uow.spimex_trading_results.add_one(schema.model_dump())
            await uow.commit()

