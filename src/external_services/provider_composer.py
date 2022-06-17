import os
from typing import Iterator, Tuple

from src.modules.nft.domain import (
    Collection, CollectionStats, Token,
    Erc20, CollectionTransaction,
)
from .etherscan_scraper import EtherScanScraper
from .opensea import OpenSea
from .moralis import Moralis
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
        self.moralis = Moralis(
            base_url=os.getenv('MORALIS_HOST'),
            api_key=os.getenv('MORALIS_KEY'),
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
    ) -> Iterator[Tuple[Token, str]]:
        results = self.opensea.get_tokens_of_collection(
            contract_address, cursor)

        for r in results['assets']:
            token = Token.create(contract_address, r)
            yield token, results['next']

    def fetch_erc20(self, contract_address: str) -> Erc20:
        result = self.moralis.get_erc20_metadata(contract_address)

        if len(result) == 0:
            return
        if result[0]['name'] == '':
            return

        erc20 = Erc20.create(result[0])
        return erc20

    def fetch_collection_transfer_activity(
        self, contract_address: str,
        from_date: str = None, to_date: str = None,
        cursor: str = None,
    ) -> Tuple[CollectionTransaction, str]:
        response = self.moralis.get_trade_activity_of_collection(
            contract_address=contract_address,
            from_date=from_date,
            to_date=to_date,
            cursor=cursor,
        )

        for r in response['result']:
            next_cursor = response['cursor']
            if response['total'] < response['page_size']:
                next_cursor = None

            txn = CollectionTransaction.create(contract_address, r)
            if not txn.currency_token:
                erc20 = self.fetch_erc20(r['price_token_address'])
                txn.set_currency_token(erc20.symbol)

            yield txn, next_cursor
