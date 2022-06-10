from sqlalchemy import Float, String, Column, DateTime, Integer
from src.databases.schema_base import DeclarativeBase, Base, DateTimestamp


class CollectionStatSchema(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'collection_stats'

    id = Column(Integer, primary_key=True)

    contract_address = Column(String, nullable=False)

    one_day_volume = Column(Float, nullable=True)
    one_day_change = Column(Float, nullable=True)
    one_day_sales = Column(Integer, nullable=True)
    one_day_average_price = Column(Float, nullable=True)

    seven_day_volume = Column(Float, nullable=True)
    seven_day_change = Column(Float, nullable=True)
    seven_day_sales = Column(Integer, nullable=True)
    seven_day_average_price = Column(Float, nullable=True)

    thirty_day_volume = Column(Float, nullable=True)
    thirty_day_change = Column(Float, nullable=True)
    thirty_day_sales = Column(Integer, nullable=True)
    thirty_day_average_price = Column(Float, nullable=True)

    total_volume = Column(Float, nullable=True)
    total_sales = Column(Integer, nullable=True)
    total_supply = Column(Integer, nullable=True)
    total_minted = Column(Integer, nullable=True)
    num_owners = Column(Integer, nullable=True)

    average_price = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    floor_price = Column(Float, nullable=True)

    updated_date = Column(DateTime(timezone=True), nullable=True)
