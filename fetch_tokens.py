import os
from sqlalchemy.orm import sessionmaker, scoped_session
from src.databases.connection import db_engine, bind_session
from src.dependencies import Dependencies
from src.modules.nft.domain import Collection, Chain, ContractType

# TODO:
# Use click in the near future
engine = db_engine(os.getenv('DATABASE_URI'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = bind_session(engine, scoped_session(SessionLocal))()

deps = Dependencies.init_real(session)
records = deps.collection_repository.find()

for r in records:
    collection = Collection(
        contract_address=r.contract_address,
        name=r.name,
        symbol=r.symbol,
        chain=Chain(r.chain),
        type=ContractType(r.type),
        logo=r.logo,
        description=r.description,
        official_site=r.official_site,
        created_date=r.created_date,
        provider_payload=r.provider_payload,
    )

    last_cursor = None
    fetch_iterator = deps.fetch_tokens_usecase.execute(collection)
    for token in fetch_iterator:
        current_cursor = deps.fetch_tokens_usecase.current_cursor
        print(token)
        deps.session.commit()
