from ..interface import ICollectionRepository
from ..models import CollectionSchema, CollectionStatSchema


class CollectionRepository(ICollectionRepository):
    def __init__(self, session):
        self.session = session
        self.model = CollectionSchema

    def get_stats(self, contract_address: str) -> CollectionStatSchema:
        q = self.session.query(CollectionStatSchema)
        q = q.filter(CollectionStatSchema.contract_address == contract_address)

        return q.first()
