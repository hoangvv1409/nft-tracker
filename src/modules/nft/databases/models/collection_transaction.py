from sqlalchemy.dialects import postgresql
from sqlalchemy import Integer, String, Column, JSON, DateTime, DECIMAL
from src.databases.schema_base import DeclarativeBase, Base, DateTimestamp


class CollectionTransactionSchema(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'collection_transactions'

    id = Column(Integer, primary_key=True)

    transaction_hash = Column(String, unique=True)
    contract_address = Column(String, nullable=False)

    token_ids = Column(
        postgresql.ARRAY(String, dimensions=1), nullable=False)
    seller_address = Column(String, nullable=False)
    buyer_address = Column(String, nullable=True)

    price = Column(DECIMAL, nullable=False)
    token_address = Column(String, nullable=True)
    currency_token = Column(String, nullable=True)

    provider_payload = Column(JSON, nullable=False)
    block_timestamp = Column(DateTime(timezone=True), nullable=False)
