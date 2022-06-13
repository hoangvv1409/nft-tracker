import os
from typing import Iterator, Tuple

from src.modules.nft.domain import Collection, CollectionStats, Token
from .etherscan_scraper import EtherScanScraper
from .opensea import OpenSea
from .provider_composer_interface import IProviderComposer


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

    def fetch_collections_and_stats_iterator(
        self, page: int = 1, page_size: int = 100,
    ) -> Iterator[Tuple[Collection, CollectionStats]]:
        results = self.etherscan.get_all_collections(
            page=page,
            page_size=page_size,
        )

        for r in results:
            stats = None
            collection = self.fetch_collection(r['contract_address'])
            if collection.opensea_slug:
                stats = self.fetch_collection_stats(
                    slug=collection.opensea_slug)

            yield collection, stats

    def fetch_collection(self, contract_address: str) -> Collection:
        addr = contract_address.lower()
        response = self.opensea.get_collection_metadata(addr)

        return Collection.create(response)

    def fetch_collection_stats(
        self, contract_address: str, slug: str = None,
    ) -> CollectionStats:
        if slug:
            response = self.opensea.get_collection_stats(slug)
            return CollectionStats.create(contract_address, response)

        if contract_address:
            raise

    def fetch_tokens(
        self, contract_address: str, cursor=None,
    ) -> Iterator[Token]:
        pass
