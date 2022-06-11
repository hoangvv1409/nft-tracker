import json
from pathlib import Path
from typing import List, Optional, Iterator
from src.modules.nft.domain import Collection

from src.external_services import IProviderComposer
from src.modules.nft.usecases import FetchCollections
from src.modules.nft.databases.interface import ICollectionRepository
from src.modules.nft.databases.models import CollectionSchema

path = Path(__file__).parent / \
    '../api_response/opensea/collection.json'
f = open(path)
payload = json.load(f)

collection_results = [
    Collection.create(payload),
    Collection.create(payload),
]


class MockProviderComposer(IProviderComposer):
    def fetch_collections(
        self, page: int = 1, page_size: int = 100,
    ) -> List[Collection]:
        pass

    def fetch_collections_iterator(
        self, page: int = 1, page_size: int = 100,
    ) -> Iterator[Collection]:
        for r in collection_results:
            yield r


class TestFetchCollection:
    def test_get_non_exist_fetch_collection(self):
        class MockCollectionRepo(ICollectionRepository):
            def first(self, **conditions) -> Optional[CollectionSchema]:
                assert 'contract_address' in conditions
                return None

            def create_from_schema(
                self, obj: CollectionSchema, flush=True, mapping=None,
            ) -> CollectionSchema:
                assert isinstance(obj, CollectionSchema)
                return obj

        fetch_collection = FetchCollections(
            api_client=MockProviderComposer(),
            collection_repository=MockCollectionRepo(),
        )
        collection = next(fetch_collection.execute())

        assert isinstance(collection, Collection)
