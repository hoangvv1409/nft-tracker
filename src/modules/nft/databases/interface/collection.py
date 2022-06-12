from abc import ABC, abstractmethod
from src.databases.repo_base import CRUD

from ..models import CollectionSchema, CollectionStatSchema


class ICollectionRepository(ABC, CRUD[CollectionSchema]):
    @abstractmethod
    def get_stats(self, contract_address: str) -> CollectionStatSchema:
        pass
