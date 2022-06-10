import json
from pathlib import Path
from src.modules.nft.domain import CollectionStats


class TestCollectionStats:
    def test_create_collection_stats_from_open_sea(self):
        path = Path(__file__).parent / \
            '../api_response/opensea/collection_stats.json'
        f = open(path)
        payload = json.load(f)
        bored_ape_contract_address =\
            '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'

        stats = CollectionStats.create(bored_ape_contract_address, payload)

        payload = payload['stats']
        assert stats.contract_address == bored_ape_contract_address
        assert stats.one_day_volume == payload['one_day_volume']
        assert stats.one_day_change == payload['one_day_change']
        assert stats.one_day_sales == payload['one_day_sales']
        assert stats.one_day_average_price == payload['one_day_average_price']

        assert stats.seven_day_volume == payload['seven_day_volume']
        assert stats.seven_day_change == payload['seven_day_change']
        assert stats.seven_day_sales == payload['seven_day_sales']
        assert stats.seven_day_average_price ==\
            payload['seven_day_average_price']

        assert stats.thirty_day_volume == payload['thirty_day_volume']
        assert stats.thirty_day_change == payload['thirty_day_change']
        assert stats.thirty_day_sales == payload['thirty_day_sales']
        assert stats.thirty_day_average_price ==\
            payload['thirty_day_average_price']

        assert stats.total_volume == payload['total_volume']
        assert stats.total_sales == payload['total_sales']
        assert stats.total_supply == payload['total_supply']
        assert stats.total_minted == payload['count']
        assert stats.num_owners == payload['num_owners']

        assert stats.average_price == payload['average_price']
        assert stats.market_cap == payload['market_cap']
        assert stats.floor_price == payload['floor_price']
