import os
import pytest

from src.external_services.opensea import OpenSea
from src.external_services.base import (
    BadRequest, InternalServerError, NotFound)

client = OpenSea(
    base_url=os.getenv('OPENSEA_HOST'),
    api_key=os.getenv('OPENSEA_KEY'),
)


class TestOpenseaGetCollection:
    def test_get_collection_metadata_with_valid_address(self):
        bored_ape_contract_address =\
            '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'

        response = client.get_collection_metadata(
            contract_address=bored_ape_contract_address
        )

        assert response['address'].lower(
        ) == bored_ape_contract_address.lower()

        assert response['symbol'] == 'BAYC'
        assert response['schema_name'] == 'ERC721'
        assert response['name'] == 'BoredApeYachtClub'

    def test_get_collection_metadata_with_invalid_contract_address(self):
        invalid_contract =\
            '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D2947829svwqq4'

        with pytest.raises(InternalServerError) as e:
            client.get_collection_metadata(
                contract_address=invalid_contract,
            )

            print(str(e))

    def test_get_collection_metadata_with_non_exist_contract_address(self):
        invalid_contract =\
            '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13E'

        with pytest.raises(NotFound) as e:
            client.get_collection_metadata(
                contract_address=invalid_contract,
            )

            print(str(e))


class TestOpenseaGetCollectionStat:
    def test_get_collection_stats_with_valid_slug(self):
        bored_ape_opensea_slug = 'boredapeyachtclub'

        response = client.get_collection_stats(
            slug=bored_ape_opensea_slug,
        )

        assert 'stats' in response

    def test_get_collection_stats_with_not_exist_slug(self):
        bored_ape_opensea_slug = 'non_exist_slug'

        with pytest.raises(NotFound) as e:
            client.get_collection_stats(
                slug=bored_ape_opensea_slug,
            )

            print(str(e))


class TestOpenseaGetNftOfCollection:
    def test_get_nft_of_collection_with_valid_address(self):
        bored_ape_contract_address =\
            '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'

        response = client.get_tokens_of_collection(
            contract_address=bored_ape_contract_address
        )

        assert 'assets' in response
        assert 'next' in response
        assert response['next'] is not None
        assert response['previous'] is None
        assert len(response['assets']) == 50

        response = client.get_tokens_of_collection(
            contract_address=bored_ape_contract_address,
            cursor=response['next'],
        )

        assert 'assets' in response
        assert 'next' in response
        assert response['next'] is not None
        assert response['previous'] is not None
        assert len(response['assets']) == 50

    def test_get_nft_of_collection_with_invalid_contract_address(self):
        invalid_contract =\
            '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D2947829svwqq4'

        with pytest.raises(BadRequest) as e:
            client.get_tokens_of_collection(
                contract_address=invalid_contract,
            )

            print(str(e))

    def test_get_nft_of_collection_with_non_exist_contract_address(self):
        invalid_contract =\
            '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13E'

        response = client.get_tokens_of_collection(
            contract_address=invalid_contract,
        )

        assert response['next'] is None
        assert response['previous'] is None
        assert len(response['assets']) == 0
