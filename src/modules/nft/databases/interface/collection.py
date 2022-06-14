from typing import List, Tuple
from abc import ABC, abstractmethod
from src.databases.repo_base import CRUD

from ..models import CollectionSchema, CollectionStatSchema


class ICollectionRepository(ABC, CRUD[CollectionSchema]):
    @abstractmethod
    def get_stats(self, contract_address: str) -> CollectionStatSchema:
        pass

    @abstractmethod
    def get_sorted_collections(
        self, page: int = 1, page_size: int = 50,
        query: str = None, sort_by: str = None,
    ) -> Tuple[int, int, List[Tuple[CollectionSchema, CollectionStatSchema]]]:
        pass
