from typing import Tuple, List
from abc import ABC, abstractmethod
from src.databases.repo_base import CRUD
from ..models import TokenSchema


class ITokenRepository(ABC, CRUD[TokenSchema]):
    @abstractmethod
    def count(self, contract_address: str):
        pass

    @abstractmethod
    def get_sorted_tokens(
        self, contract_address: str,
        page: int = 1, page_size: int = 50,
        sort_by: str = None,
    ) -> Tuple[int, int, List[TokenSchema]]:
        pass
