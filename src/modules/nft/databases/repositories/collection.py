from src.databases.repo_base import CRUD
from ..models import CollectionSchema


class CollectionRepository(CRUD):
    def __init__(self, session):
        self.session = session
        self.model = CollectionSchema
