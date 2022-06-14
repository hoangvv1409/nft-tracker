import math
from typing import List, Tuple
from ..interface import ICollectionRepository
from ..models import CollectionSchema, CollectionStatSchema


class CollectionRepository(ICollectionRepository):
    def __init__(self, session):
        self.session = session
        self.model = CollectionSchema

    def get_stats(self, contract_address: str) -> CollectionStatSchema:
        q = self.session.query(CollectionStatSchema)
        q = q.filter(CollectionStatSchema.contract_address == contract_address)
        q = q.order_by(CollectionStatSchema.one_day_volume.desc())

        return q.first()

    def get_sorted_collections(
        self, page: int = 1, page_size: int = 50,
        query: str = None, sort_by: str = None,
    ) -> Tuple[int, int, List[Tuple[CollectionSchema, CollectionStatSchema]]]:
        sortable = [
            'one_day_volume', 'seven_day_volume',
            'floor_price', 'one_day_sales', 'created_date',
        ]
        if sort_by and sort_by not in sortable:
            raise

        q = self.session.query(CollectionSchema, CollectionStatSchema)
        q = q.join(
            CollectionStatSchema,
            CollectionSchema.contract_address
            == CollectionStatSchema.contract_address
        )

        if query:
            search = '%{}%'.format(query)
            q = q.filter(CollectionSchema.name.ilike(search))

        if sort_by == 'created_date':
            q = q.order_by(CollectionSchema.created_date.desc())
        elif sort_by:
            q = q.order_by(getattr(CollectionStatSchema, sort_by).desc())
        count = q.count()

        q = q.limit(page_size)
        q = q.offset((page - 1) * page_size)
        records = q.all()

        total_page = math.ceil(count / page_size)

        return count, total_page, records
