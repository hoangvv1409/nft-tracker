from abc import ABC, abstractmethod
from typing import Iterator, Tuple

from src.modules.nft.domain import Collection, CollectionStats


class IProviderComposer(ABC):
    @abstractmethod
    def fetch_collections_iterator(
        self, page: int = 1, page_size: int = 100,
    ) -> Iterator[Collection]:
        pass

    @abstractmethod
    def fetch_collection(self, contract_address: str) -> Collection:
        pass

    @abstractmethod
    def fetch_collection_stats(
        self, contract_address: str, slug: str = None,
    ) -> CollectionStats:
        pass

    @abstractmethod
    def fetch_collections_and_stats_iterator(
        self, page: int = 1, page_size: int = 100,
    ) -> Iterator[Tuple[Collection, CollectionStats]]:
        pass
