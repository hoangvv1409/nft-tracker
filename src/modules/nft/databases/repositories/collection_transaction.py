from ..interface import ICollectionTransactionRepository
from ..models import CollectionTransactionSchema


class CollectionTransactionRepository(ICollectionTransactionRepository):
    def __init__(self, session):
        self.session = session
        self.model = CollectionTransactionSchema
