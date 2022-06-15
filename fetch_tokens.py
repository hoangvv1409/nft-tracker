import os
import sys
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


def main(id, max_worker):
    for r in records:
        if r.id % max_worker != id:
            continue

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
        stats = deps.collection_repository.get_stats(
            collection.contract_address)
        if not stats:
            continue

        count = deps.token_repository.count(collection.contract_address)

        if count >= stats.total_supply:
            continue

        last_cursor = None
        fetch_iterator = deps.fetch_tokens_usecase.execute(collection)
        for token in fetch_iterator:
            current_cursor = deps.fetch_tokens_usecase.current_cursor

            if last_cursor != current_cursor:
                print(f'-----Cursor {current_cursor}-----')
                last_cursor = current_cursor

            print(token)
            deps.session.commit()

            if not current_cursor:
                fetch_iterator.close()


if __name__ == "__main__":
    id = 1
    max_worker = 3
    if len(sys.argv) > 1:
        id = int(sys.argv[1])

    main(id, max_worker)
