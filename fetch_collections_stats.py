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
fetch_iterator = deps.fetch_collections_stats_usecase.execute()
last_page = 0

for i in fetch_iterator:
    print(i[0])
    deps.session.commit()
