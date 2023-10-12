import datetime
import asyncio
from typing import Literal

import xlrd
import httpx

from config import settings
from schemas import SpimexTradingResultSchemaAdd


async def parse_all_data(links: list[str]) -> list[SpimexTradingResultSchemaAdd]:
    tasks = set()
    schemas = []
    for link in links:
        tasks.add(asyncio.create_task(parse_data(link)))
    error_tasks = 0
    for task in tasks:
        try:
            this_schemas = await task
        except httpx._exceptions.HTTPError:
            error_tasks += 1
            continue
        else:
            schemas.extend(this_schemas)
    print(f"Excel parse error tasks count: {error_tasks}")
    return schemas


async def parse_data(link: str) -> list[SpimexTradingResultSchemaAdd]:
    sheet = await download_sheet(link)
    start_row, end_row = search_section_with_unit(sheet, 'Метрическая тонна')
    schemas = convert_section_data_in_schemas(sheet, start_row, end_row)
    return schemas


async def download_sheet(link: str) -> xlrd.sheet.Sheet:
    async with httpx.AsyncClient() as client:
        res = await client.get(f'{settings.BASE_URL}{link}', timeout=None)
    return xlrd.open_workbook(file_contents=res.content, formatting_info=True).sheet_by_index(0)


def search_section_with_unit(sheet: xlrd.sheet.Sheet, unit: Literal['Метрическая тонна']) -> tuple[int, int]:
    start_row: int | None = None
    end_row: int | None = None
    for row in range(sheet.nrows):
        if sheet.cell_value(row, 1) == f'Единица измерения: {unit}':
            start_row = row
    for row in range(start_row, sheet.nrows):
        if sheet.cell_value(row, 1) == 'Итого:':
            end_row = row
    if start_row is None or end_row is None:
        return []
    start_row += 4
    return start_row, end_row


def convert_section_data_in_schemas(
        sheet: xlrd.sheet.Sheet,
        start_row: int,
        end_row: int
) -> list[SpimexTradingResultSchemaAdd]:
    schemas = []
    for row in range(start_row, end_row):
        if sheet.cell_value(row, 4) != '-':
            exchange_product_id = sheet.cell_value(row, 1)
            schemas.append(SpimexTradingResultSchemaAdd(
                exchange_product_id=exchange_product_id,
                exchange_product_name=sheet.cell_value(row, 2),
                oil_id=exchange_product_id[:4],
                delivery_basis_id=exchange_product_id[4:7],
                delivery_basis_name=sheet.cell_value(row, 3),
                delivery_type_id=exchange_product_id[-1],
                volume=sheet.cell_value(row, 4),
                total=sheet.cell_value(row, 5),
                count=sheet.cell_value(row, 14),
                date=datetime.datetime.strptime(sheet.cell_value(3, 1)[13:], settings.DATETIME_FORMAT).date()
            ))
    return schemas
