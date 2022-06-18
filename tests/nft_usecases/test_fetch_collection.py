import json
from pathlib import Path
from typing import Optional, Iterator, Tuple, List
from src.modules.nft.domain import (
    Collection, CollectionStats, Token,
    Erc20, CollectionTransaction,
)

from src.external_services import IProviderComposer
from src.modules.nft.usecases import FetchCollections
from src.modules.nft.databases.interface import ICollectionRepository
from src.modules.nft.databases.models import (
    CollectionSchema, CollectionStatSchema)

path = Path(__file__).parent / \
    '../api_response/opensea/collection.json'
f = open(path)
payload = json.load(f)

collection_results = [
    Collection.create(payload),
    Collection.create(payload),
]


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
        pass

    def fetch_collections_and_stats_iterator(
        self, page: int = 1, page_size: int = 100,
    ) -> Iterator[Tuple[Collection, CollectionStats]]:
        pass

    def fetch_tokens(
        self, contract_address: str, cursor=None,
    ) -> Iterator[Token]:
        pass

    def fetch_erc20(self, contract_address: str) -> Erc20:
        pass

    def fetch_collection_transfer_activity(
        self, contract_address: str,
        from_date: str = None, to_date: str = None,
        cursor: str = None,
    ) -> Tuple[CollectionTransaction, str]:
        pass


class TestFetchCollection:
    def test_get_non_exist_collection(self):
        class MockCollectionRepo(ICollectionRepository):
            def first(self, **conditions) -> Optional[CollectionSchema]:
                assert 'contract_address' in conditions
                return None

            def create_from_schema(
                self, obj: CollectionSchema, flush=True, mapping=None,
            ) -> CollectionSchema:
                assert isinstance(obj, CollectionSchema)
                return obj

            def get_stats(self, contract_address: str) -> CollectionStatSchema:
                pass

            def get_sorted_collections(
                self, page: int = 1, page_size: int = 50,
                query: str = None, sort_by: str = None,
            ) -> Tuple[
                int, int, List[Tuple[CollectionSchema, CollectionStatSchema]]
            ]:
                pass

        fetch_collection = FetchCollections(
            api_client=MockProviderComposer(),
            collection_repository=MockCollectionRepo(),
        )
        collection = next(fetch_collection.execute())

        assert isinstance(collection, Collection)
