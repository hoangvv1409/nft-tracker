from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass
from .collection import ApiProvider


@dataclass
class CollectionTransaction:
    transaction_hash: str
    contract_address: str
    token_ids: List[str]

    seller_address: str
    buyer_address: str
    block_timestamp: datetime

    price: int
    token_address: str = None
    currency_token: str = None

    provider_payload: Dict = None

    @staticmethod
    def create(
        contract_address: str, response: Dict,
        provider: ApiProvider = ApiProvider.MORALIS,
    ):
        if provider == ApiProvider.MORALIS:
            return CollectionTransaction._create_from_moralis(
                contract_address, response,
            )

    @staticmethod
    def _create_from_moralis(contract_address: str, response: Dict):
        currency_token = None
        if not response['price_token_address']:
            currency_token = 'ETH'

        return CollectionTransaction(
            transaction_hash=response['transaction_hash'],
            contract_address=contract_address,
            token_ids=response['token_ids'],
            seller_address=response['seller_address'],
            buyer_address=response['buyer_address'],
            block_timestamp=response['block_timestamp'],
            price=int(response['price']),
            token_address=response['token_address'],
            currency_token=currency_token,
            provider_payload={'moralis': response},
        )

    def set_currency_token(self, token: str = 'ETH'):
        if self.currency_token is None:
            self.currency_token = token

    def __repr__(self):
        response = 'Txn Hash: {} | Tokens: {} | Addr: {}'.format(
            self.transaction_hash,
            ','.join(self.token_ids),
            self.contract_address,
        )
        return response
