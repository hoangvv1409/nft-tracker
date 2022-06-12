from typing import Any
from dataclasses import dataclass

from src.external_services.provider_composer import (
    IProviderComposer, ProviderComposer,
)

from src.modules.nft.databases.interface import ICollectionRepository
from src.modules.nft.databases.repositories import CollectionRepository

from src.modules.nft.usecases import FetchCollections, FetchCollectionsStats


@dataclass()
class Dependencies:
    session: Any
    api_client: IProviderComposer
    collection_repository: ICollectionRepository

    fetch_collections_usecase: FetchCollections
    fetch_collections_stats_usecase: FetchCollectionsStats

    @staticmethod
    def init_real(session):
        api_client = ProviderComposer()
        collection_repo = CollectionRepository(session)
        fetch_collections_usecase = FetchCollections(
            api_client=api_client,
            collection_repository=collection_repo,
        )
        fetch_collections_stats_usecase = FetchCollectionsStats(
            api_client=api_client,
            collection_repository=collection_repo,
        )

        return Dependencies(
            session=session,
            api_client=api_client,
            collection_repository=collection_repo,
            fetch_collections_usecase=fetch_collections_usecase,
            fetch_collections_stats_usecase=fetch_collections_stats_usecase,
        )

    @staticmethod
    def init_fake():
        return None
