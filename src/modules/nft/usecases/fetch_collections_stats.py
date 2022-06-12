from typing import Iterator, Tuple

from src.utils import domain_model_to_orm_schema_mapper
from src.modules.nft.domain import (
    Collection, CollectionStats, Chain, ContractType)
from ..databases.models import CollectionStatSchema

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
            # TODO: move this to common mapper
            collection = Collection(
                contract_address=collection_orm.contract_address,
                name=collection_orm.name,
                symbol=collection_orm.symbol,
                chain=Chain(collection_orm.chain),
                type=ContractType(collection_orm.type),
                logo=collection_orm.logo,
                description=collection_orm.description,
                official_site=collection_orm.official_site,
                created_date=collection_orm.created_date,
                provider_payload=collection_orm.provider_payload,
            )
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

        # TODO: update collection case
        if not stats_orm:
            self.collection_repo.create_from_schema(stats_schema)
