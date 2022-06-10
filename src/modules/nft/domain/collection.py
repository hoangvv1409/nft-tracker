import pytz
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


@dataclass
class CollectionStats:
    contract_address: str

    one_day_volume: float
    one_day_change: float
    one_day_sales: int
    one_day_average_price: float

    seven_day_volume: float
    seven_day_change: float
    seven_day_sales: int
    seven_day_average_price: float

    thirty_day_volume: float
    thirty_day_change: float
    thirty_day_sales: int
    thirty_day_average_price: float

    total_volume: float
    total_sales: int
    total_supply: int
    total_minted: int
    num_owners: int

    average_price: float
    market_cap: float
    floor_price: float

    updated_date: datetime

    @staticmethod
    def create(
        contract_address: str, response: Dict,
        provider: ApiProvider = ApiProvider.OPENSEA,
    ):
        if provider == ApiProvider.OPENSEA:
            return CollectionStats._create_from_opensea(
                contract_address, response)

    @staticmethod
    def _create_from_opensea(contract_address: str, response: Dict):
        response = response['stats']
        floor_price = 0.0
        if response['floor_price']:
            floor_price = response['floor_price']

        return CollectionStats(
            contract_address=contract_address,
            one_day_volume=response['one_day_volume'],
            one_day_change=response['one_day_change'],
            one_day_sales=response['one_day_sales'],
            one_day_average_price=response['one_day_average_price'],

            seven_day_volume=response['seven_day_volume'],
            seven_day_change=response['seven_day_change'],
            seven_day_sales=response['seven_day_sales'],
            seven_day_average_price=response['seven_day_average_price'],

            thirty_day_volume=response['thirty_day_volume'],
            thirty_day_change=response['thirty_day_change'],
            thirty_day_sales=response['thirty_day_sales'],
            thirty_day_average_price=response['thirty_day_average_price'],

            total_volume=response['total_volume'],
            total_sales=response['total_sales'],
            total_supply=response['total_supply'],
            total_minted=response['count'],
            num_owners=response['num_owners'],

            average_price=response['average_price'],
            market_cap=response['market_cap'],
            floor_price=floor_price,

            updated_date=datetime.now(pytz.utc),
        )
