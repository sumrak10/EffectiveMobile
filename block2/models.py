import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from schemas import SpimexTradingResultSchema


class SpimexTradingResults(Base):
    __tablename__ = 'spimex_trading_results'
    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[int]
    total: Mapped[int]
    count: Mapped[int]
    date: Mapped[datetime.date]
    created_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())

    def get_schema(self) -> SpimexTradingResultSchema:
        return SpimexTradingResultSchema(
            id=self.id,
            exchange_product_id=self.exchange_product_id,
            exchange_product_name=self.exchange_product_name,
            oil_id=self.oil_id,
            delivery_basis_id=self.delivery_basis_id,
            delivery_basis_name=self.delivery_basis_name,
            delivery_type_id=self.delivery_type_id,
            volume=self.volume,
            total=self.total,
            count=self.count,
            date=self.date,
            created_on=self.created_on,
            updated_on=self.updated_on
        )
