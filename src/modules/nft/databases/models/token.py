from sqlalchemy import Integer, String, Column, JSON, DateTime, DECIMAL
from src.databases.schema_base import DeclarativeBase, Base, DateTimestamp


class TokenSchema(DeclarativeBase, Base, DateTimestamp):
    # unique token_id + contract_address
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)

    token_id = Column(String, nullable=False)
    contract_address = Column(String, nullable=False)

    token_metadata = Column(JSON, nullable=True)
    provider_payload = Column(JSON, nullable=True)

    current_price = Column(DECIMAL, nullable=True)
    last_price = Column(DECIMAL, nullable=True)
    owner_address = Column(String, nullable=True)
    transfer_token = Column(String, nullable=True)
    block_timestamp = Column(DateTime(timezone=True), nullable=False)
