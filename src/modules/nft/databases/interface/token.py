from abc import ABC, abstractmethod
from src.databases.repo_base import CRUD
from ..models import TokenSchema


class ITokenRepository(ABC, CRUD[TokenSchema]):
    @abstractmethod
    def count(self, contract_address: str):
        pass
