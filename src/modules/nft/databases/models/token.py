from sqlalchemy import Integer, String, Column, JSON
from src.databases.schema_base import DeclarativeBase, Base, DateTimestamp


class TokenSchema(DeclarativeBase, Base, DateTimestamp):
    # unique token_id + contract_address
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)

    token_id = Column(String, nullable=False)
    contract_address = Column(String, nullable=False)

    metadata = Column(JSON, nullable=True)
    provider_payload = Column(JSON, nullable=True)
