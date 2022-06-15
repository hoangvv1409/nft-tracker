from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import TypeVar, Type, List, Optional, Generic

from .schema_base import Base

T = TypeVar('T')


class Duplicate(Exception):
    pass


class CRUD(Generic[T]):
    session: Type[Session] = None
    model: Type[Base] = None

    def __init__(self, session=None, model=None):
        self.session = session
        self.model = model

    def find_by_id(self, model_id) -> Optional[T]:
        q = self.session.query(self.model).filter(self.model.id == model_id)
        return q.first()

    def find(self, **conditions) -> List[T]:
        query = self.session.query(self.model)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)

        return query.all()

    def find_paging(self, limit=None, offset=None, **conditions) -> List[T]:
        query = self.session.query(self.model)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)

        if limit is not None and offset is not None:
            return query.count(), query.limit(limit).offset(offset).all()
        else:
            records = query.all()
            return len(records), records

    def first(self, **conditions) -> Optional[T]:
        query = self.session.query(self.model)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)

        return query.first()

    def create_from_schema(
        self, obj: T, flush=True, mapping=None,
    ) -> T:
        try:
            self.session.add(obj)
            if flush:
                self.session.flush()
            return obj
        except exc.IntegrityError as e:
            raise e

    def create(self, flush=True, mapping=None, **data) -> T:
        try:
            obj = self.model()
            for key in data:
                p = key
                if mapping and key in mapping:
                    p = mapping.get(key)

                if hasattr(obj, key):
                    setattr(obj, key, data[p])

            self.session.add(obj)
            if flush:
                self.session.flush()
            return obj
        except exc.IntegrityError as e:
            # raise e
            raise {
                # '23503': UUnprocessableEntity,
                '23505': Duplicate(e.orig.pgerror)
            }[e.orig.pgcode] or exc.IntegrityError

    def update(self, obj, flush=True, only=None, **data) -> T:
        if obj:
            for k in data:
                if k.startswith('_'):
                    continue

                if hasattr(obj, k) and (only is None or k in only):
                    setattr(obj, k, data.get(k))
        if flush:
            self.session.flush()
        return obj

    def bulk_update(self, records):
        return self.session.bulk_update_mappings(self.model, records)

    def delete(self, obj, flush=True) -> bool:
        try:
            self.session.delete(obj)
            if flush:
                self.session.flush()
            return True
        except exc.IntegrityError as e:
            raise e
