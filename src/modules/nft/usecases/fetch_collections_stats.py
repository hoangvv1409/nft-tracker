from typing import Iterator, Tuple

from src.utils import domain_model_to_orm_schema_mapper
from src.modules.nft.domain import Collection, CollectionStats
from ..databases.models import CollectionStatSchema
from .mapper import collection_orm_to_model

from src.external_services import IProviderComposer
from ..databases.interface import ICollectionRepository


class FetchCollectionsStats:
    def __init__(
        self, api_client: IProviderComposer,
        collection_repository: ICollectionRepository,
    ):
        self.api_client = api_client
        self.collection_repo = collection_repository

    def execute(self) -> Iterator[Tuple[Collection, CollectionStats]]:
        collections_orm = self.collection_repo.find()
        for collection_orm in collections_orm:
            collection = collection_orm_to_model(collection_orm)
            try:
                stats = self.api_client.fetch_collection_stats(
                    contract_address=collection.contract_address,
                    slug=collection.opensea_slug,
                )
            # TODO: Handling exception here (Notfound, BadRequest, ...)
            except:
                continue

            self._collection_stats_handler(stats)
            yield collection, stats

    def _collection_stats_handler(self, stats: CollectionStats):
        stats_orm = self.collection_repo.get_stats(
            contract_address=stats.contract_address)
        stats_schema = domain_model_to_orm_schema_mapper(
            schema=CollectionStatSchema,
            domain_model=stats,
        )

        if not stats_orm:
            self.collection_repo.create_from_schema(stats_schema)
        else:
            self.collection_repo.update(stats_orm, **stats_schema.__dict__)
