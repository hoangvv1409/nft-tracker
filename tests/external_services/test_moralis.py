import os
import pytest

from src.external_services.moralis import Moralis
from src.external_services.base import BadRequest, NotFound


class TestMoralis:
    def test_get_collection_metadata_with_valid_address(self):
        bored_ape_contract_address =\
            '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'

        client = Moralis(
            base_url=os.getenv('MORALIS_HOST'),
            api_key=os.getenv('MORALIS_KEY'),
        )

        response = client.get_collection_metadata(
            contract_address=bored_ape_contract_address
        )

        assert response['token_address'].lower(
        ) == bored_ape_contract_address.lower()

        assert response['symbol'] == 'BAYC'
        assert response['contract_type'] == 'ERC721'
        assert response['name'] == 'BoredApeYachtClub'

    def test_get_collection_metadata_with_invalid_chain(self):
        bored_ape_contract_address =\
            '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'

        client = Moralis(
            base_url=os.getenv('MORALIS_HOST'),
            api_key=os.getenv('MORALIS_KEY'),
        )

        with pytest.raises(BadRequest) as e:
            client.get_collection_metadata(
                contract_address=bored_ape_contract_address,
                chain='yolo',
            )

            print(str(e))

    def test_get_collection_metadata_with_invalid_contract_address(self):
        invalid_contract =\
            '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D2947829svwqq4'

        client = Moralis(
            base_url=os.getenv('MORALIS_HOST'),
            api_key=os.getenv('MORALIS_KEY'),
        )

        with pytest.raises(BadRequest) as e:
            client.get_collection_metadata(
                contract_address=invalid_contract,
            )

            print(str(e))

    def test_get_collection_metadata_with_non_exist_contract_address(self):
        invalid_contract =\
            '0xBC4CA0EdA7647A8aB7C2061c2E118A19'

        client = Moralis(
            base_url=os.getenv('MORALIS_HOST'),
            api_key=os.getenv('MORALIS_KEY'),
        )

        with pytest.raises(NotFound) as e:
            client.get_collection_metadata(
                contract_address=invalid_contract,
            )

            print(str(e))
