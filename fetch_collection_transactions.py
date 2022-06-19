import os
import pdb
import sys
from sqlalchemy.orm import sessionmaker, scoped_session
from src.databases.connection import db_engine, bind_session
from src.dependencies import Dependencies
from src.modules.nft.domain import Collection, Chain, ContractType
from src.databases.repo_base import Duplicate

# TODO:
# Use click in the near future
engine = db_engine(os.getenv('DATABASE_URI'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = bind_session(engine, scoped_session(SessionLocal))()

deps = Dependencies.init_real(session)
records = deps.collection_repository.find()


def main(
    id, max_worker,
    from_date: str = None,
    to_date: str = None,
):
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

        last_cursor = None
        fetch_iterator = deps.fetch_collection_transaction_usecase.execute(
            collection=collection,
            from_date=from_date,
            to_date=to_date,
        )

        print(f'-----Cursor {last_cursor}-----')

        for txn in fetch_iterator:
            current_cursor =\
                deps.fetch_collection_transaction_usecase.current_cursor

            if last_cursor != current_cursor:
                print(f'-----Cursor {current_cursor}-----')
                last_cursor = current_cursor

            print(txn)

            try:
                deps.session.commit()
            except Duplicate:
                deps.session.rollback()


if __name__ == "__main__":
    id = 1
    max_worker = 3
    from_date = None
    to_date = None

    if len(sys.argv) >= 2:
        id = int(sys.argv[1])
    if len(sys.argv) >= 3:
        from_date = sys.argv[2]
    if len(sys.argv) >= 4:
        to_date = sys.argv[3]

    main(id, max_worker, from_date, to_date)
