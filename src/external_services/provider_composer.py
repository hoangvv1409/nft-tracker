import os
from typing import Iterator
from abc import ABC, abstractmethod

from src.modules.nft.domain import Collection
from .etherscan_scraper import EtherScanScraper
from .opensea import OpenSea


class IProviderComposer(ABC):
    @abstractmethod
    def fetch_collections_iterator(
        self, page: int = 1, page_size: int = 100,
    ) -> Iterator[Collection]:
        pass

    @abstractmethod
    def fetch_collection(self, contract_address: str) -> Collection:
        pass


class ProviderComposer(IProviderComposer):
    # FIXME:
    # env should be injected
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
            collection = self.fetch_collection(r['contract_address'])
            yield collection

    def fetch_collection(self, contract_address: str) -> Collection:
        addr = contract_address.lower()
        response = self.opensea.get_collection_metadata(addr)

        return Collection.create(response)
