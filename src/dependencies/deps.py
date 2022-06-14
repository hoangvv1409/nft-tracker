from tokenize import Token
from typing import Any
from dataclasses import dataclass

from src.external_services.provider_composer import (
    IProviderComposer, ProviderComposer,
)

from src.modules.nft.databases.interface import (
    ICollectionRepository, ITokenRepository)
from src.modules.nft.databases.repositories import (
    CollectionRepository, TokenRepository)

from src.modules.nft.usecases import (
    FetchCollections, FetchCollectionsStats, FetchTokens,
)


@dataclass()
class Dependencies:
    session: Any
    api_client: IProviderComposer
    collection_repository: ICollectionRepository
    token_repository: ITokenRepository

    fetch_collections_usecase: FetchCollections
    fetch_collections_stats_usecase: FetchCollectionsStats
    fetch_tokens_usecase: FetchTokens

    @staticmethod
    def init_real(session):
        api_client = ProviderComposer()
        collection_repo = CollectionRepository(session)
        token_repo = TokenRepository(session)

        fetch_collections_usecase = FetchCollections(
            api_client=api_client,
            collection_repository=collection_repo,
        )
        fetch_collections_stats_usecase = FetchCollectionsStats(
            api_client=api_client,
            collection_repository=collection_repo,
        )
        fetch_token_usecase = FetchTokens(
            api_client=api_client,
            token_repository=token_repo,
        )

        return Dependencies(
            session=session,
            api_client=api_client,

            collection_repository=collection_repo,
            token_repository=token_repo,

            fetch_collections_usecase=fetch_collections_usecase,
            fetch_collections_stats_usecase=fetch_collections_stats_usecase,
            fetch_tokens_usecase=fetch_token_usecase,
        )

    @staticmethod
    def init_fake():
        return None
