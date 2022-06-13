import json
from pathlib import Path
from typing import List, Iterator, Tuple
from src.modules.nft.domain import Collection, CollectionStats, Token

from src.external_services import IProviderComposer
from src.modules.nft.usecases import FetchCollectionsStats
from src.modules.nft.databases.interface import ICollectionRepository
from src.modules.nft.databases.models import (
    CollectionStatSchema, CollectionSchema)
from src.utils import domain_model_to_orm_schema_mapper

contract_address = '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d'
path = Path(__file__).parent / \
    '../api_response/opensea/collection.json'
f = open(path)
payload = json.load(f)

collection_results = [
    Collection.create(payload),
    Collection.create(payload),
]

path = Path(__file__).parent / \
    '../api_response/opensea/collection_stats.json'
f = open(path)
stats_payload = json.load(f)


class MockProviderComposer(IProviderComposer):
    def fetch_collection(self, contract_address: str) -> Collection:
        pass

    def fetch_collections_iterator(
        self, page: int = 1, page_size: int = 100,
    ) -> Iterator[Collection]:
        for r in collection_results:
            yield r

    def fetch_collection_stats(
        self, contract_address: str = None, slug: str = None,
    ) -> CollectionStats:
        return CollectionStats.create(contract_address, stats_payload)

    def fetch_collections_and_stats_iterator(
        self, page: int = 1, page_size: int = 100,
    ) -> Iterator[Tuple[Collection, CollectionStats]]:
        pass

    def fetch_tokens(
        self, contract_address: str, cursor=None,
    ) -> Iterator[Token]:
        pass


class TestFetchCollectionStats:
    def test_get_non_exist_stats(self):
        class MockCollectionRepo(ICollectionRepository):
            def find(self, **conditions) -> List[CollectionSchema]:
                assert conditions == {}
                return [
                    domain_model_to_orm_schema_mapper(
                        CollectionSchema, collection_results[0]),
                    domain_model_to_orm_schema_mapper(
                        CollectionSchema, collection_results[1]),
                ]

            def create_from_schema(
                self, obj: CollectionStatSchema, flush=True, mapping=None,
            ) -> CollectionStatSchema:
                assert isinstance(obj, CollectionStatSchema)

            def get_stats(self, contract_address: str) -> CollectionStatSchema:
                assert contract_address is not None
                assert contract_address != ''
                return None

        fetch_collection_stats = FetchCollectionsStats(
            api_client=MockProviderComposer(),
            collection_repository=MockCollectionRepo(),
        )
        collection, stats = next(fetch_collection_stats.execute())

        assert isinstance(collection, Collection)
        assert isinstance(stats, CollectionStats)
