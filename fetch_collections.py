import os
from sqlalchemy.orm import sessionmaker, scoped_session
from src.databases.connection import db_engine, bind_session
from src.dependencies import Dependencies

# TODO:
# Use click in the near future
engine = db_engine(os.getenv('DATABASE_URI'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = bind_session(engine, scoped_session(SessionLocal))()

deps = Dependencies.init_real(session)
fetch_iterator = deps.fetch_collections_usecase.execute()
last_page = 0

for collection in fetch_iterator:
    current_page = deps.fetch_collections_usecase.current_page
    if last_page != current_page:
        print(f'-----Page {current_page}-----')
        last_page = current_page

    print(collection)
    deps.session.commit()
