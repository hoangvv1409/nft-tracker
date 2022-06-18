from datetime import datetime
from typing import Dict
from dataclasses import dataclass
from .collection import ApiProvider


@dataclass
class Erc20:
    address: str
    name: str
    symbol: str
    created_at: datetime

    provider_payload: Dict = None

    @staticmethod
    def create(
        response: Dict, provider: ApiProvider = ApiProvider.MORALIS,
    ):
        if provider == ApiProvider.MORALIS:
            return Erc20._create_from_moralis(response)

    @staticmethod
    def _create_from_moralis(response: Dict):
        return Erc20(
            address=response['address'],
            name=response['name'],
            symbol=response['symbol'],
            created_at=response.get('created_at'),
            provider_payload={'moralis': response},
        )

    def __repr__(self):
        response = 'Name: {} | Addr: {} | Symbol: {}'.format(
            self.name,
            self.address,
            self.symbol,
        )
        return response
