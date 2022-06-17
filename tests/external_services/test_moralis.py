import os
import pytest

from src.external_services.moralis import Moralis
from src.external_services.base import BadRequest, NotFound

client = Moralis(
    base_url=os.getenv('MORALIS_HOST'),
    api_key=os.getenv('MORALIS_KEY'),
)

bored_ape_contract_address =\
    '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'
invalid_contract =\
    '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D2947829svwqq4'
erc20_usdc_contract_address = \
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
non_exist_contract_address = \
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb49'


class TestMoralis:
    def test_get_collection_metadata_with_valid_address(self):
        response = client.get_collection_metadata(
            contract_address=bored_ape_contract_address
        )

        assert response['token_address'].lower(
        ) == bored_ape_contract_address.lower()

        assert response['symbol'] == 'BAYC'
        assert response['contract_type'] == 'ERC721'
        assert response['name'] == 'BoredApeYachtClub'

    def test_get_collection_metadata_with_invalid_chain(self):
        with pytest.raises(BadRequest) as e:
            client.get_collection_metadata(
                contract_address=bored_ape_contract_address,
                chain='yolo',
            )

            print(str(e))

    def test_get_collection_metadata_with_invalid_contract_address(self):
        with pytest.raises(BadRequest) as e:
            client.get_collection_metadata(
                contract_address=invalid_contract,
            )

            print(str(e))

    def test_get_collection_metadata_with_non_exist_contract_address(self):
        with pytest.raises(NotFound) as e:
            client.get_collection_metadata(
                contract_address=non_exist_contract_address,
            )

            print(str(e))

    def test_get_erc20_metadata(self):
        response = client.get_erc20_metadata(
            contract_address=erc20_usdc_contract_address
        )

        assert len(response) == 1
        assert response[0]['address'].lower(
        ) == erc20_usdc_contract_address.lower()

        assert response[0]['symbol'] == 'USDC'
        assert response[0]['name'] == 'USD Coin'

    def test_get_erc20_metadata_with_invalid_contract_address(self):
        with pytest.raises(BadRequest) as e:
            client.get_collection_metadata(
                contract_address=invalid_contract,
            )

            print(str(e))

    def test_get_erc20_metadata_with_non_exist_contract_address(self):
        with pytest.raises(NotFound) as e:
            client.get_collection_metadata(
                contract_address=non_exist_contract_address,
            )

            print(str(e))

    def test_get_trade_activity_of_collection(self):
        response = client.get_trade_activity_of_collection(
            contract_address=bored_ape_contract_address,
        )

        assert response['cursor'] != ''
        assert len(response['result']) == 50

    def test_get_trade_activity_of_collection_with_non_exist_contract(self):
        response = client.get_trade_activity_of_collection(
            contract_address=non_exist_contract_address,
        )

        assert response['cursor'] == ''
        assert len(response['result']) == 0

    def test_get_trade_activity_of_collection_with_invalid_contract(self):
        with pytest.raises(BadRequest) as e:
            client.get_trade_activity_of_collection(
                contract_address=invalid_contract,
            )

            print(str(e))
