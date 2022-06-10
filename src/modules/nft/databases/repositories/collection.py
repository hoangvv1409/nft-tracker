from ..interface import ICollectionRepository
from ..models import CollectionSchema


class CollectionRepository(ICollectionRepository):
    def __init__(self, session):
        self.session = session
        self.model = CollectionSchema
