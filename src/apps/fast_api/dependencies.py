import os
from fastapi import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import sessionmaker, scoped_session
from src.databases.connection import db_engine, bind_session
from src.dependencies import Dependencies

engine = db_engine(os.getenv('DATABASE_URI'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
token_auth_scheme = HTTPBearer()


def get_session():
    session = bind_session(engine, scoped_session(SessionLocal))()
    try:
        yield session
    finally:
        session.close()


def resolve_dependencies(
    session: str = Depends(get_session)
) -> Dependencies:
    return Dependencies.init_real(session)
