import json
from pathlib import Path
from src.modules.nft.domain import Collection, Chain, ContractType

path = Path(__file__).parent / \
    '../api_response/opensea/collection.json'
f = open(path)
payload = json.load(f)


class TestCollection:
    def test_create_collection_from_open_sea(self):
        collection = Collection.create(payload)

        assert collection.contract_address == payload['address']
        assert collection.symbol == payload['symbol']
        assert collection.name == payload['name']
        assert collection.chain == Chain.ETH
        assert collection.type == ContractType.ERC721

        assert collection.logo == payload['image_url']
        assert collection.description == payload['description']
        assert collection.official_site == payload['external_link']
        assert collection.created_date == payload['created_date']
        assert collection.provider_payload['opensea'] == payload

        assert str(collection) == 'Name: {} | Symbol: {} | Addr: {}'.format(
            payload['name'],
            payload['symbol'],
            payload['address'],
        )

    def test_opensea_slug_property_when_opensea_payload_exist(self):
        collection = Collection.create(payload)
        assert collection.opensea_slug == 'boredapeyachtclub'

    def test_opensea_slug_property_when_opensea_payload_non_exist(self):
        collection = Collection.create(payload)
        collection.provider_payload.pop('opensea', None)

        assert collection.opensea_slug is None
