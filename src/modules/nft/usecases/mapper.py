from ..domain import (
    Collection, Chain, ContractType,
    Token, TokenAttribute, TokenMetadata,
)
from ..databases.models import CollectionSchema, TokenSchema


def collection_orm_to_model(orm: CollectionSchema) -> Collection:
    return Collection(
        contract_address=orm.contract_address,
        name=orm.name,
        symbol=orm.symbol,
        chain=Chain(orm.chain),
        type=ContractType(orm.type),
        logo=orm.logo,
        description=orm.description,
        official_site=orm.official_site,
        created_date=orm.created_date,
        provider_payload=orm.provider_payload,
    )


def token_orm_to_model(orm: TokenSchema) -> Token:
    attrs = []
    for attr in orm.token_metadata['attributes']:
        attrs.append(
            TokenAttribute(
                trait_type=attr['trait_type'],
                value=attr['value'],
                trait_count=attr['trait_count'],
            )
        )

    token_metadata = TokenMetadata(
        name=orm.token_metadata['name'],
        description=orm.token_metadata['description'],
        image_url=orm.token_metadata['image_url'],
        metadata_url=orm.token_metadata['metadata_url'],
        attributes=attrs
    )
    token = Token(
        token_id=orm.token_id,
        contract_address=orm.contract_address,
        provider_payload=orm.provider_payload,
        token_metadata=token_metadata
    )

    return token
