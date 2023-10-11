import datetime
import asyncio

import httpx
from bs4 import BeautifulSoup

from config import settings


async def get_links_for_period(
        start_date: datetime.date,
        end_date: datetime.date
) -> list[str]:
    links = []
    tasks = set()
    tasks_count = round((start_date - end_date).days / 7 * 5 / 10)
    for i in range(1, tasks_count+1):
        tasks.add(asyncio.create_task(get_page_links(i, end_date)))
    error_tasks = 0
    for task in tasks:
        try:
            this_links = await task
        except httpx._exceptions.HTTPError:
            error_tasks += 1
            continue
        else:
            links.extend(this_links)
    print(f"BS4 parse error tasks count: {error_tasks}")
    return links


async def get_page_links(i: int, end_date: datetime.date) -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{settings.BASE_URL}/markets/oil_products/trades/results/',
            params={'page': f'page-{i}'}
        )
    links = []
    soup = BeautifulSoup(
        response.text,
        features="html.parser"
    )
    accordion_items = soup.find('div', {'class': 'page-content__tabs__block'}) \
        .find_all('div', {'class': 'accordeon-inner__item'})
    for accordion_item in accordion_items:
        link_url: str = accordion_item.find('a', {'class': 'accordeon-inner__item-title link xls'}).get('href')
        last_date = datetime.datetime.strptime(
            accordion_item.find('span').contents[0],
            settings.DATETIME_FORMAT
        ).date()
        if last_date >= end_date:
            links.append(link_url)
    return links
