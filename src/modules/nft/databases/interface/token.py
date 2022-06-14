from abc import ABC
from src.databases.repo_base import CRUD
from ..models import TokenSchema


class ITokenRepository(ABC, CRUD[TokenSchema]):
    pass
