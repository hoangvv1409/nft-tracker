import time
from typing import Iterator

from src.utils import domain_model_to_orm_schema_mapper
from src.modules.nft.domain import Collection
from ..databases.models import CollectionSchema

from src.external_services import IProviderComposer
from ..databases.interface import ICollectionRepository


class FetchCollections:
    def __init__(
        self, api_client: IProviderComposer,
        collection_repository: ICollectionRepository,
        current_page: int = 1, sleep: int = 0.5,
    ):
        self.sleep = sleep
        self.current_page = current_page

        self.api_client = api_client
        self.collection_repo = collection_repository

    def execute(
        self, page_size: int = 100, max_page: int = 20,
    ) -> Iterator[Collection]:
        while self.current_page <= max_page:
            collection_iterator = self.api_client.fetch_collections_iterator(
                page=self.current_page,
                page_size=page_size,
            )

            for collection in collection_iterator:
                self._collection_handler(collection)
                yield collection

            self.current_page += 1
            time.sleep(self.sleep)

    def _collection_handler(self, collection: Collection):
        addr = collection.contract_address
        # skip Ethereum Name Service (ENS)
        if addr == '0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85':
            return

        collection_orm = self.collection_repo.first(contract_address=addr)
        collection_schema = domain_model_to_orm_schema_mapper(
            schema=CollectionSchema,
            domain_model=collection,
        )

        # TODO: update collection case
        if not collection_orm:
            self.collection_repo.create_from_schema(collection_schema)
