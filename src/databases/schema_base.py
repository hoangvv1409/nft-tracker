from datetime import datetime
from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class Base(object):
    def __init__(self, **data):
        for key, value in data.iteritems():
            setattr(self, key, value)


class DateTimestamp():
    _created_at = Column(TIMESTAMP, nullable=True, default=datetime.utcnow)
    _updated_at = Column(TIMESTAMP, nullable=True, onupdate=datetime.utcnow,
                         default=datetime.utcnow)
