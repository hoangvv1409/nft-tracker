from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, field
from .collection import ApiProvider


@dataclass
class TokenAttribute:
    trait_type: str
    value: str
    trait_count: int = None


@dataclass
class TokenMetadata:
    name: str
    description: str
    image_url: str
    metadata_url: str = None
    attributes: List[TokenAttribute] = field(default_factory=lambda: [])


@dataclass
class Token:
    token_id: str
    contract_address: str

    token_metadata: TokenMetadata

    creator_address: str = None
    provider_payload: Dict = None

    current_price: int = None
    last_price: int = None
    owner_address: str = None
    block_timestamp: datetime = None
    transfer_token: str = None

    @staticmethod
    def create(
        contract_address: str, response: Dict,
        provider: ApiProvider = ApiProvider.OPENSEA,
    ):
        if provider == ApiProvider.OPENSEA:
            return Token._create_from_opensea(contract_address, response)

    def transfer(
        self, price: int, transfer_token: str,
        owner_address: str, block_timestamp: datetime,
    ):
        self.last_price = self.current_price
        self.current_price = price
        self.transfer_token = transfer_token
        self.owner_address = owner_address
        self.block_timestamp = block_timestamp

    @staticmethod
    def _create_from_opensea(contract_address: str, response: Dict):
        attrs = []
        for trait in response['traits']:
            attrs.append(TokenAttribute(
                trait_type=trait['trait_type'],
                value=trait['value'],
                trait_count=trait['trait_count'],
            ))

        metadata = TokenMetadata(
            name=response['name'],
            description=response['description'],
            image_url=response['image_original_url'],
            metadata_url=response['token_metadata'],
            attributes=attrs,
        )

        # creator_address = None
        # if response['creator']:
        #     creator_address = response['creator']['address']

        return Token(
            token_id=response['token_id'],
            contract_address=contract_address,
            token_metadata=metadata,
            # creator_address=creator_address,
            provider_payload={'opensea': response},
        )

    def __repr__(self):
        response = 'Token Id: {} | Name: {} | Addr: {} | Link: {}'.format(
            self.token_id,
            self.token_metadata.name,
            self.contract_address,
            self.token_metadata.image_url,
        )
        return response
