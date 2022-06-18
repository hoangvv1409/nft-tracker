from abc import ABC
from src.databases.repo_base import CRUD
from ..models import CollectionTransactionSchema


class ICollectionTransactionRepository(ABC, CRUD[CollectionTransactionSchema]):
    pass
