import os
import pytest

from src.external_services.opensea import OpenSea
from src.external_services.base import InternalServerError, NotFound

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
    def test_collection_stats_with_valid_slug(self):
        bored_ape_opensea_slug = 'boredapeyachtclub'

        response = client.get_collection_stats(
            slug=bored_ape_opensea_slug,
        )

        assert 'stats' in response

    def test_collection_stats_with_not_exist_slug(self):
        bored_ape_opensea_slug = 'non_exist_slug'

        with pytest.raises(NotFound) as e:
            client.get_collection_stats(
                slug=bored_ape_opensea_slug,
            )
