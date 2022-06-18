import json
from pathlib import Path

from src.modules.nft.domain import Token

path = Path(__file__).parent / \
    '../api_response/opensea/tokens.json'
f = open(path)
payload = json.load(f)
bored_ape_contract_address =\
    '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'


class TestToken:
    def test_create_token_from_open_sea(self):
        token_payload = payload['assets'][0]
        token = Token.create(bored_ape_contract_address, token_payload)

        assert token.token_id == token_payload['token_id']
        assert token.contract_address == bored_ape_contract_address
        assert token.creator_address == token_payload['creator']['address']
        assert token.provider_payload['opensea'] == token_payload
        metadata = token.token_metadata
        assert metadata.name == token_payload['name']
        assert metadata.description == token_payload['description']
        assert metadata.image_url == token_payload['image_original_url']
        assert metadata.metadata_url == token_payload['token_metadata']
        assert len(token.token_metadata.attributes) == len(
            token_payload['traits'])
        for idx, attr in enumerate(token.token_metadata.attributes):
            attr.__dict__ == token_payload['traits'][idx]
