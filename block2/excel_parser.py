import datetime
import asyncio

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
    async with httpx.AsyncClient() as client:
        res = await client.get(f'{settings.BASE_URL}{link}', timeout=None)
    sheet = xlrd.open_workbook(file_contents=res.content, formatting_info=True).sheet_by_index(0)
    date = datetime.datetime.strptime(sheet.cell_value(3, 1)[13:], settings.DATETIME_FORMAT).date()

    start_row: int | None = None
    end_row: int | None = None
    for row in range(sheet.nrows):
        if sheet.cell_value(row, 1) == 'Единица измерения: Метрическая тонна':
            start_row = row
    for row in range(start_row, sheet.nrows):
        if sheet.cell_value(row, 1) == 'Итого:':
            end_row = row
    if start_row is None or end_row is None:
        return []
    start_row += 4
    # end_row += 1

    schemas = []
    for row in range(start_row, end_row):
        if sheet.cell_value(row, 4) != '-':
            exchange_product_id = sheet.cell_value(row, 1)
            exchange_product_name = sheet.cell_value(row, 2)
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
                date=date
            ))
    return schemas


# linkss = ['/upload/reports/oil_xls/oil_xls_20231011162000.xls?r=5322', '/upload/reports/oil_xls/oil_xls_20231010162000.xls?r=4832', '/upload/reports/oil_xls/oil_xls_20231009162000.xls?r=1322', '/upload/reports/oil_xls/oil_xls_20231006162000.xls?r=4268', '/upload/reports/oil_xls/oil_xls_20231005162000.xls?r=2211', '/upload/reports/oil_xls/oil_xls_20231004162000.xls?r=7648', '/upload/reports/oil_xls/oil_xls_20231003162000.xls?r=3287', '/upload/reports/oil_xls/oil_xls_20231002162000.xls?r=4576', '/upload/reports/oil_xls/oil_xls_20230929162000.xls?r=9018', '/upload/reports/oil_xls/oil_xls_20230928162000.xls?r=4276', '/upload/reports/oil_xls/oil_xls_20230927162000.xls?r=8027', '/upload/reports/oil_xls/oil_xls_20230926162000.xls?r=5428', '/upload/reports/oil_xls/oil_xls_20230925162000.xls?r=7875', '/upload/reports/oil_xls/oil_xls_20230922162000.xls?r=8549', '/upload/reports/oil_xls/oil_xls_20230921162000.xls?r=2472', '/upload/reports/oil_xls/oil_xls_20230920162000.xls?r=6067', '/upload/reports/oil_xls/oil_xls_20230919162000.xls?r=1438', '/upload/reports/oil_xls/oil_xls_20230918162000.xls?r=1840', '/upload/reports/oil_xls/oil_xls_20230915162000.xls?r=6943', '/upload/reports/oil_xls/oil_xls_20230914162000.xls?r=3551', '/upload/reports/oil_xls/oil_xls_20230913162000.xls?r=5753', '/upload/reports/oil_xls/oil_xls_20230912162000.xls?r=3018', '/upload/reports/oil_xls/oil_xls_20230911162000.xls?r=2153', '/upload/reports/oil_xls/oil_xls_20230908162000.xls?r=9503', '/upload/reports/oil_xls/oil_xls_20230907162000.xls?r=2253', '/upload/reports/oil_xls/oil_xls_20230906162000.xls?r=8159', '/upload/reports/oil_xls/oil_xls_20230905162000.xls?r=1545', '/upload/reports/oil_xls/oil_xls_20230904162000.xls?r=7707', '/upload/reports/oil_xls/oil_xls_20230901162000.xls?r=7003', '/upload/reports/oil_xls/oil_xls_20230831162000.xls?r=9065', '/upload/reports/oil_xls/oil_xls_20230830162000.xls?r=9469', '/upload/reports/oil_xls/oil_xls_20230829162000.xls?r=3758', '/upload/reports/oil_xls/oil_xls_20230828162000.xls?r=2630', '/upload/reports/oil_xls/oil_xls_20230825162000.xls?r=3644', '/upload/reports/oil_xls/oil_xls_20230824162000.xls?r=1611', '/upload/reports/oil_xls/oil_xls_20230823162000.xls?r=1268', '/upload/reports/oil_xls/oil_xls_20230822162000.xls?r=1484', '/upload/reports/oil_xls/oil_xls_20230821162000.xls?r=9312', '/upload/reports/oil_xls/oil_xls_20230818162000.xls?r=8370', '/upload/reports/oil_xls/oil_xls_20230817162000.xls?r=7949', '/upload/reports/oil_xls/oil_xls_20230816162000.xls?r=8469', '/upload/reports/oil_xls/oil_xls_20230815162000.xls?r=2349', '/upload/reports/oil_xls/oil_xls_20230814162000.xls?r=5841', '/upload/reports/oil_xls/oil_xls_20230811162000.xls?r=4590', '/upload/reports/oil_xls/oil_xls_20230810162000.xls?r=5567', '/upload/reports/oil_xls/oil_xls_20230809162000.xls?r=2375', '/upload/reports/oil_xls/oil_xls_20230808162000.xls?r=6587', '/upload/reports/oil_xls/oil_xls_20230807162000.xls?r=3505', '/upload/reports/oil_xls/oil_xls_20230804162000.xls?r=8484', '/upload/reports/oil_xls/oil_xls_20230803162000.xls?r=7496', '/upload/reports/oil_xls/oil_xls_20230802162000.xls?r=6085', '/upload/reports/oil_xls/oil_xls_20230801162000.xls?r=6016', '/upload/reports/oil_xls/oil_xls_20230731162000.xls?r=8483', '/upload/reports/oil_xls/oil_xls_20230728162000.xls?r=9405', '/upload/reports/oil_xls/oil_xls_20230727162000.xls?r=9170', '/upload/reports/oil_xls/oil_xls_20230726162000.xls?r=3554', '/upload/reports/oil_xls/oil_xls_20230725162000.xls?r=2381', '/upload/reports/oil_xls/oil_xls_20230724162000.xls?r=6424', '/upload/reports/oil_xls/oil_xls_20230721162000.xls?r=4321', '/upload/reports/oil_xls/oil_xls_20230720162000.xls?r=2578', '/upload/reports/oil_xls/oil_xls_20230719162000.xls?r=8827', '/upload/reports/oil_xls/oil_xls_20230718162000.xls?r=3170', '/upload/reports/oil_xls/oil_xls_20230717162000.xls?r=5273', '/upload/reports/oil_xls/oil_xls_20230714162000.xls?r=7315', '/upload/reports/oil_xls/oil_xls_20230713162000.xls?r=4604', '/upload/reports/oil_xls/oil_xls_20230712162000.xls?r=3847', '/upload/reports/oil_xls/oil_xls_20230711162000.xls?r=1005', '/upload/reports/oil_xls/oil_xls_20230710162000.xls?r=7680', '/upload/reports/oil_xls/oil_xls_20230707162000.xls?r=6986', '/upload/reports/oil_xls/oil_xls_20230706162000.xls?r=6540', '/upload/reports/oil_xls/oil_xls_20230705162000.xls?r=8996', '/upload/reports/oil_xls/oil_xls_20230704162000.xls?r=6476', '/upload/reports/oil_xls/oil_xls_20230703162000.xls?r=4887', '/upload/reports/oil_xls/oil_xls_20230630162000.xls?r=1637', '/upload/reports/oil_xls/oil_xls_20230629162000.xls?r=9555', '/upload/reports/oil_xls/oil_xls_20230628162000.xls?r=5288', '/upload/reports/oil_xls/oil_xls_20230627162000.xls?r=5187', '/upload/reports/oil_xls/oil_xls_20230626162000.xls?r=5109', '/upload/reports/oil_xls/oil_xls_20230623162000.xls?r=8566', '/upload/reports/oil_xls/oil_xls_20230622162000.xls?r=7480', '/upload/reports/oil_xls/oil_xls_20230621162000.xls?r=6604', '/upload/reports/oil_xls/oil_xls_20230620162000.xls?r=7556', '/upload/reports/oil_xls/oil_xls_20230619162000.xls?r=1455', '/upload/reports/oil_xls/oil_xls_20230616162000.xls?r=7795', '/upload/reports/oil_xls/oil_xls_20230615162000.xls?r=4901', '/upload/reports/oil_xls/oil_xls_20230614162000.xls?r=5809', '/upload/reports/oil_xls/oil_xls_20230613162000.xls?r=1108', '/upload/reports/oil_xls/oil_xls_20230609162000.xls?r=2475', '/upload/reports/oil_xls/oil_xls_20230608162000.xls?r=4217', '/upload/reports/oil_xls/oil_xls_20230607162000.xls?r=9186', '/upload/reports/oil_xls/oil_xls_20230606162000.xls?r=4492', '/upload/reports/oil_xls/oil_xls_20230605162000.xls?r=7031', '/upload/reports/oil_xls/oil_xls_20230602162000.xls?r=9501', '/upload/reports/oil_xls/oil_xls_20230601162000.xls?r=6109', '/upload/reports/oil_xls/oil_xls_20230531162000.xls?r=4417', '/upload/reports/oil_xls/oil_xls_20230530162000.xls?r=4819', '/upload/reports/oil_xls/oil_xls_20230529162000.xls?r=2347', '/upload/reports/oil_xls/oil_xls_20230526162000.xls?r=8955', '/upload/reports/oil_xls/oil_xls_20230525162000.xls?r=7680', '/upload/reports/oil_xls/oil_xls_20230524162000.xls?r=7516', '/upload/reports/oil_xls/oil_xls_20230523162000.xls?r=5362', '/upload/reports/oil_xls/oil_xls_20230522162000.xls?r=6338', '/upload/reports/oil_xls/oil_xls_20230519162000.xls?r=5740', '/upload/reports/oil_xls/oil_xls_20230518162000.xls?r=2611', '/upload/reports/oil_xls/oil_xls_20230517162000.xls?r=4886', '/upload/reports/oil_xls/oil_xls_20230516162000.xls?r=9219', '/upload/reports/oil_xls/oil_xls_20230515162000.xls?r=7885', '/upload/reports/oil_xls/oil_xls_20230512162000.xls?r=6858', '/upload/reports/oil_xls/oil_xls_20230511162000.xls?r=2803', '/upload/reports/oil_xls/oil_xls_20230510162000.xls?r=9031', '/upload/reports/oil_xls/oil_xls_20230505162000.xls?r=9658', '/upload/reports/oil_xls/oil_xls_20230504162000.xls?r=1147', '/upload/reports/oil_xls/oil_xls_20230503162000.xls?r=2126', '/upload/reports/oil_xls/oil_xls_20230502162000.xls?r=7676', '/upload/reports/oil_xls/oil_xls_20230428162000.xls?r=1700', '/upload/reports/oil_xls/oil_xls_20230427162000.xls?r=6615', '/upload/reports/oil_xls/oil_xls_20230426162000.xls?r=8033', '/upload/reports/oil_xls/oil_xls_20230425162000.xls?r=2037', '/upload/reports/oil_xls/oil_xls_20230424162000.xls?r=3287', '/upload/reports/oil_xls/oil_xls_20230421162000.xls?r=5876', '/upload/reports/oil_xls/oil_xls_20230420162000.xls?r=6364', '/upload/reports/oil_xls/oil_xls_20230419162000.xls?r=7224', '/upload/reports/oil_xls/oil_xls_20230418162000.xls?r=4576', '/upload/reports/oil_xls/oil_xls_20230417162000.xls?r=7281', '/upload/reports/oil_xls/oil_xls_20230414162000.xls?r=3069', '/upload/reports/oil_xls/oil_xls_20230413162000.xls?r=4358', '/upload/reports/oil_xls/oil_xls_20230412162000.xls?r=8395', '/upload/reports/oil_xls/oil_xls_20230411162000.xls?r=9118', '/upload/reports/oil_xls/oil_xls_20230410162000.xls?r=3248', '/upload/reports/oil_xls/oil_xls_20230407162000.xls?r=8434', '/upload/reports/oil_xls/oil_xls_20230406162000.xls?r=7457', '/upload/reports/oil_xls/oil_xls_20230405162000.xls?r=4715', '/upload/reports/oil_xls/oil_xls_20230404162000.xls?r=9629', '/upload/reports/oil_xls/oil_xls_20230403162000.xls?r=9479', '/upload/reports/oil_xls/oil_xls_20230331162000.xls?r=3593', '/upload/reports/oil_xls/oil_xls_20230330162000.xls?r=1050', '/upload/reports/oil_xls/oil_xls_20230329162000.xls?r=4438', '/upload/reports/oil_xls/oil_xls_20230328162000.xls?r=8978', '/upload/reports/oil_xls/oil_xls_20230327162000.xls?r=2874', '/upload/reports/oil_xls/oil_xls_20230324162000.xls?r=9661', '/upload/reports/oil_xls/oil_xls_20230323162000.xls?r=9024', '/upload/reports/oil_xls/oil_xls_20230322162000.xls?r=7146', '/upload/reports/oil_xls/oil_xls_20230321162000.xls?r=2864', '/upload/reports/oil_xls/oil_xls_20230320162000.xls?r=2496', '/upload/reports/oil_xls/oil_xls_20230317162000.xls?r=7613', '/upload/reports/oil_xls/oil_xls_20230316162000.xls?r=3321', '/upload/reports/oil_xls/oil_xls_20230315162000.xls?r=4088', '/upload/reports/oil_xls/oil_xls_20230314162000.xls?r=3293', '/upload/reports/oil_xls/oil_xls_20230313162000.xls?r=3954', '/upload/reports/oil_xls/oil_xls_20230310162000.xls?r=7160', '/upload/reports/oil_xls/oil_xls_20230309162000.xls?r=8772', '/upload/reports/oil_xls/oil_xls_20230307162000.xls?r=4406', '/upload/reports/oil_xls/oil_xls_20230306162000.xls?r=9995', '/upload/reports/oil_xls/oil_xls_20230303162000.xls?r=2888', '/upload/reports/oil_xls/oil_xls_20230302162000.xls?r=8370', '/upload/reports/oil_xls/oil_xls_20230301162000.xls?r=2831', '/upload/reports/oil_xls/oil_xls_20230228162000.xls?r=2191', '/upload/reports/oil_xls/oil_xls_20230227162000.xls?r=9575', '/upload/reports/oil_xls/oil_xls_20230222162000.xls?r=1733', '/upload/reports/oil_xls/oil_xls_20230221162000.xls?r=4329', '/upload/reports/oil_xls/oil_xls_20230220162000.xls?r=6389', '/upload/reports/oil_xls/oil_xls_20230217162000.xls?r=8831', '/upload/reports/oil_xls/oil_xls_20230216162000.xls?r=1744', '/upload/reports/oil_xls/oil_xls_20230215162000.xls?r=6991', '/upload/reports/oil_xls/oil_xls_20230214162000.xls?r=8849', '/upload/reports/oil_xls/oil_xls_20230213162000.xls?r=1550', '/upload/reports/oil_xls/oil_xls_20230210162000.xls?r=2410', '/upload/reports/oil_xls/oil_xls_20230209162000.xls?r=1320', '/upload/reports/oil_xls/oil_xls_20230208162000.xls?r=1539', '/upload/reports/oil_xls/oil_xls_20230207162000.xls?r=2156', '/upload/reports/oil_xls/oil_xls_20230206162000.xls?r=1180', '/upload/reports/oil_xls/oil_xls_20230203162000.xls?r=5666', '/upload/reports/oil_xls/oil_xls_20230202162000.xls?r=8022', '/upload/reports/oil_xls/oil_xls_20230201162000.xls?r=7863', '/upload/reports/oil_xls/oil_xls_20230131162000.xls?r=5857', '/upload/reports/oil_xls/oil_xls_20230130162000.xls?r=1667', '/upload/reports/oil_xls/oil_xls_20230127162000.xls?r=6906', '/upload/reports/oil_xls/oil_xls_20230126162000.xls?r=8789', '/upload/reports/oil_xls/oil_xls_20230125162000.xls?r=8434', '/upload/reports/oil_xls/oil_xls_20230124162000.xls?r=4172', '/upload/reports/oil_xls/oil_xls_20230123162000.xls?r=6101', '/upload/reports/oil_xls/oil_xls_20230120162000.xls?r=5984', '/upload/reports/oil_xls/oil_xls_20230119162000.xls?r=3090', '/upload/reports/oil_xls/oil_xls_20230118162000.xls?r=5090', '/upload/reports/oil_xls/oil_xls_20230117162000.xls?r=1971', '/upload/reports/oil_xls/oil_xls_20230116162000.xls?r=1193', '/upload/reports/oil_xls/oil_xls_20230113162000.xls?r=8134', '/upload/reports/oil_xls/oil_xls_20230112162000.xls?r=1664', '/upload/reports/oil_xls/oil_xls_20230111162000.xls?r=5519', '/upload/reports/oil_xls/oil_xls_20230110162000.xls?r=7205', '/upload/reports/oil_xls/oil_xls_20230109162000.xls?r=1827']
#
# async def main():
#     schemas = await parse_all_data(linkss)
#
# asyncio.run(main())
