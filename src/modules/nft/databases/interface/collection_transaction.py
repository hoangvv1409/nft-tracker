from typing import Tuple, List
from abc import ABC, abstractmethod
from src.databases.repo_base import CRUD
from ..models import CollectionTransactionSchema


class ICollectionTransactionRepository(ABC, CRUD[CollectionTransactionSchema]):
    @abstractmethod
    def get_sorted_transactions(
        self, contract_address: str,
        page: int = 1, page_size: int = 50,
    ) -> Tuple[int, int, List[CollectionTransactionSchema]]:
        pass
