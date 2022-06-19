from typing import Iterator, List

from src.utils import domain_model_to_orm_schema_mapper
from src.modules.nft.domain import Collection, Token
from ..databases.models import TokenSchema

from src.external_services import IProviderComposer
from ..databases.interface import ITokenRepository


class FetchTokens:
    def __init__(
        self, api_client: IProviderComposer,
        token_repository: ITokenRepository,
        current_cursor: str = None,
    ):
        self.current_cursor = current_cursor
        self.api_client = api_client
        self.token_repo = token_repository

    def execute(self, collection: Collection) -> Iterator[List[Token]]:
        while True:
            iterator = self.api_client.fetch_tokens(
                contract_address=collection.contract_address,
                cursor=self.current_cursor,
            )
            for token, next_cursor in iterator:
                if not token.token_id:
                    continue

                self._token_handler(token)
                yield token

            self.current_cursor = next_cursor
            if not next_cursor:
                break

    def _token_handler(self, token: Token):
        token_orm = self.token_repo.first(
            contract_address=token.contract_address,
            token_id=token.token_id
        )
        token_schema = domain_model_to_orm_schema_mapper(
            schema=TokenSchema,
            domain_model=token,
        )

        # TODO: update token case
        if not token_orm:
            self.token_repo.create_from_schema(token_schema)
