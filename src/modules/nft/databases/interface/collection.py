from abc import ABC
from src.databases.repo_base import CRUD

from ..models import CollectionSchema


class ICollectionRepository(ABC, CRUD[CollectionSchema]):
    pass
