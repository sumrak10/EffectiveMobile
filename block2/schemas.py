import datetime

from pydantic import BaseModel


class SpimexTradingResultSchema(BaseModel):
    id: int
    exchange_product_id: int
    exchange_product_name: str
    oil_id: int
    delivery_basis_id: int
    delivery_basis_name: str
    delivery_type_id: int
    volume: int
    total: int
    count: int
    date: datetime.date
    created_on: datetime.datetime
    updated_on: datetime.datetime


class SpimexTradingResultSchemaAdd(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: int
    count: int
    date: datetime.date
