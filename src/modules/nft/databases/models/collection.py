from sqlalchemy import Integer, String, Column, JSON, DateTime
from src.databases.schema_base import DeclarativeBase, Base, DateTimestamp


class CollectionSchema(DeclarativeBase, Base, DateTimestamp):
    # unique contract_address + chain
    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True)

    contract_address = Column(String, nullable=False)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=True)
    chain = Column(String, nullable=False)
    type = Column(String, nullable=False)

    logo = Column(String, nullable=True)
    description = Column(String, nullable=True)
    official_site = Column(String, nullable=True)
    created_date = Column(DateTime(timezone=True), nullable=True)

    provider_payload = Column(JSON, nullable=False)
