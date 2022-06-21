from typing import Any
from dataclasses import dataclass

from src.external_services.provider_composer import (
    IProviderComposer, ProviderComposer,
)

from src.modules.nft.databases.interface import (
    ICollectionRepository, ITokenRepository, ICollectionTransactionRepository,
)
from src.modules.nft.databases.repositories import (
    CollectionRepository, TokenRepository, CollectionTransactionRepository,
)

from src.modules.nft.usecases import (
    FetchCollections, FetchCollectionsStats, FetchTokens,
    FetchCollectionTransaction,
)


@dataclass()
class Dependencies:
    session: Any
    api_client: IProviderComposer
    collection_repository: ICollectionRepository
    token_repository: ITokenRepository
    collection_transaction_repository: ICollectionTransactionRepository

    fetch_collections_usecase: FetchCollections
    fetch_collections_stats_usecase: FetchCollectionsStats
    fetch_tokens_usecase: FetchTokens
    fetch_collection_transaction_usecase: FetchCollectionTransaction

    @staticmethod
    def init_real(session):
        api_client = ProviderComposer()
        collection_repo = CollectionRepository(session)
        token_repo = TokenRepository(session)
        collection_transaction_repo = CollectionTransactionRepository(session)

        fetch_collections = FetchCollections(
            api_client=api_client,
            collection_repository=collection_repo,
        )
        fetch_collections_stats = FetchCollectionsStats(
            api_client=api_client,
            collection_repository=collection_repo,
        )
        fetch_token = FetchTokens(
            api_client=api_client,
            token_repository=token_repo,
        )
        fetch_collection_transaction = FetchCollectionTransaction(
            api_client=api_client,
            token_repository=token_repo,
            collection_transaction_repository=collection_transaction_repo,
        )

        return Dependencies(
            session=session,
            api_client=api_client,

            collection_repository=collection_repo,
            token_repository=token_repo,
            collection_transaction_repository=collection_transaction_repo,

            fetch_collections_usecase=fetch_collections,
            fetch_collections_stats_usecase=fetch_collections_stats,
            fetch_tokens_usecase=fetch_token,
            fetch_collection_transaction_usecase=fetch_collection_transaction,
        )

    @staticmethod
    def init_fake():
        return None
