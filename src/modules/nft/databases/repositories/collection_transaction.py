import math
from typing import List, Tuple
from ..interface import ICollectionTransactionRepository
from ..models import CollectionTransactionSchema


class CollectionTransactionRepository(ICollectionTransactionRepository):
    def __init__(self, session):
        self.session = session
        self.model = CollectionTransactionSchema

    def get_sorted_transactions(
        self, contract_address: str,
        page: int = 1, page_size: int = 50,
    ) -> Tuple[int, int, List[CollectionTransactionSchema]]:
        q = self.session.query(CollectionTransactionSchema)
        q = q.filter(
            CollectionTransactionSchema.contract_address == contract_address)

        count = q.count()

        q = q.limit(page_size)
        q = q.offset((page - 1) * page_size)
        records = q.all()

        total_page = math.ceil(count / page_size)

        return count, total_page, records
