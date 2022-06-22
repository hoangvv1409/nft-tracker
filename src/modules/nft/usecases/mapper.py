from ..domain import Collection, Chain, ContractType
from ..databases.models import CollectionSchema


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


def token_orm_to_model():
    pass
