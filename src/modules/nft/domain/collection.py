from enum import Enum
from typing import Dict
from datetime import datetime
from dataclasses import dataclass


class ApiProvider(Enum):
    OPENSEA = 'OPENSEA'
    MORALIS = 'MORALIS'
    ETHERSCAN = 'ETHERSCAN'


class ContractType(Enum):
    ERC721 = 'ERC721'


class Chain(Enum):
    ETH = 'ETH'


@dataclass
class Collection:
    contract_address: str
    name: str
    symbol: str
    chain: Chain
    type: ContractType

    logo: str = None
    description: str = None
    official_site: str = None
    created_date: datetime = None

    provider_payload: Dict = None

    @staticmethod
    def create(response: Dict, provider: ApiProvider = ApiProvider.OPENSEA):
        if provider == ApiProvider.OPENSEA:
            return Collection._create_from_opensea(response)

    @staticmethod
    def _create_from_opensea(response: Dict):
        return Collection(
            contract_address=response['address'].lower(),
            name=response['name'],
            symbol=response['symbol'],
            type=ContractType.ERC721,
            chain=Chain.ETH,
            logo=response['image_url'],
            description=response['description'],
            # FIXME:
            # created_date in model is datetime,
            # but mapping like this will be string
            created_date=response['created_date'],
            official_site=response['external_link'],
            provider_payload={'opensea': response},
        )

    def __repr__(self):
        response = 'Name: {} | Symbol: {} | Addr: {}'.format(
            self.name,
            self.symbol,
            self.contract_address,
        )
        return response
