import os
from typing import List, Iterator
from abc import ABC, abstractmethod

from src.modules.nft.domain import Collection
from .etherscan_scraper import EtherScanScraper
from .opensea import OpenSea


class IProviderComposer(ABC):
    @abstractmethod
    def fetch_collections(
        self, page: int = 1, page_size: int = 100,
    ) -> List[Collection]:
        pass

    @abstractmethod
    def fetch_collections_iterator(
        self, page: int = 1, page_size: int = 100,
    ) -> Iterator[Collection]:
        pass


class ProviderComposer(IProviderComposer):
    def __init__(self):
        self.etherscan = EtherScanScraper(os.getenv('ETHER_SCAN_HOST'))
        self.opensea = OpenSea(
            base_url=os.getenv('OPENSEA_HOST'),
            api_key=os.getenv('OPENSEA_KEY'),
        )

    def fetch_collections_iterator(
        self, page: int = 1, page_size: int = 100,
    ) -> Iterator[Collection]:
        results = self.etherscan.get_all_collections(
            page=page,
            page_size=page_size,
        )

        for r in results:
            collection = self._fetch_collection_metadata(
                r['contract_address'].lower()
            )
            yield collection

    def fetch_collections(
        self, page: int = 1, page_size: int = 100,
    ) -> List[Collection]:
        results = self.etherscan.get_all_collections(
            page=page,
            page_size=page_size,
        )

        collections = [
            self._fetch_collection_metadata(
                r['contract_address'].lower()
            )
            for r in results
        ]

        return collections

    def _fetch_collection_metadata(self, contract_address: str) -> Collection:
        response = self.opensea.get_collection_metadata(contract_address)
        return Collection.create(response)
