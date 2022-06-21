from typing import Iterator, List

from src.utils import domain_model_to_orm_schema_mapper
from src.modules.nft.domain import (
    Collection, CollectionTransaction,
    Token, TokenAttribute, TokenMetadata,
)
from ..databases.models import CollectionTransactionSchema, TokenSchema

from src.external_services import IProviderComposer
from ..databases.interface import (
    ICollectionTransactionRepository, ITokenRepository)


class FetchCollectionTransaction:
    def __init__(
        self, api_client: IProviderComposer,
        token_repository: ITokenRepository,
        collection_transaction_repository: ICollectionTransactionRepository,
        current_cursor: str = None,
    ):
        self.current_cursor = current_cursor
        self.api_client = api_client
        self.token_repo = token_repository
        self.collection_transaction_repo = collection_transaction_repository

    def execute(
        self, collection: Collection,
        from_date: str = None, to_date: str = None,
    ) -> Iterator[List[CollectionTransaction]]:
        while True:
            next_cursor = None
            iterator = self.api_client.fetch_collection_transfer_activity(
                contract_address=collection.contract_address,
                from_date=from_date,
                to_date=to_date,
                cursor=self.current_cursor,
            )
            for txn, next_cursor in iterator:
                self._transaction_handler(txn)
                self._update_token(txn)
                yield txn

            self.current_cursor = next_cursor
            if not next_cursor:
                break

    def _update_token(self, txn: CollectionTransaction):
        for token_id in txn.token_ids:
            token_orm = self.token_repo.first(
                token_id=token_id,
                contract_address=txn.contract_address
            )
            if not token_orm:
                continue

            token = self._map_token_orm_to_token(token_orm)
            if (not token.block_timestamp or
                    token.block_timestamp < txn.block_timestamp):
                token.transfer(
                    price=txn.price,
                    transfer_token=txn.currency_token,
                    owner_address=txn.buyer_address,
                    block_timestamp=txn.block_timestamp,
                )

            token_schema = domain_model_to_orm_schema_mapper(
                schema=TokenSchema,
                domain_model=token,
            )
            self.token_repo.update(token_orm, **token_schema.__dict__)

    def _transaction_handler(self, txn: CollectionTransaction):
        txn_orm = self.collection_transaction_repo.first(
            transaction_hash=txn.transaction_hash)
        if txn_orm:
            return

        txn_schema = domain_model_to_orm_schema_mapper(
            schema=CollectionTransactionSchema,
            domain_model=txn,
        )

        self.collection_transaction_repo.create_from_schema(txn_schema)

    def _map_token_orm_to_token(self, token_orm: TokenSchema):
        attrs = []
        for attr in token_orm.token_metadata['attributes']:
            attrs.append(
                TokenAttribute(
                    trait_type=attr['trait_type'],
                    value=attr['value'],
                    trait_count=attr['trait_count'],
                )
            )

        token = Token(
            token_id=token_orm.token_id,
            contract_address=token_orm.contract_address,
            provider_payload=token_orm.provider_payload,
            token_metadata=TokenMetadata(
                name=token_orm.token_metadata['name'],
                description=token_orm.token_metadata['description'],
                image_url=token_orm.token_metadata['image_url'],
                metadata_url=token_orm.token_metadata['metadata_url'],
                attributes=attrs
            ))
        return token
