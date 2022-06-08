import os

from src.external_services.etherscan_scraper import EtherScanScraper


class TestEtherScraper:
    def test_get_all_collections(self):
        page_size = 50
        client = EtherScanScraper(os.getenv('ETHER_SCAN_HOST'))
        response = client.get_all_collections(
            page=1, page_size=page_size
        )
        assert len(response) == page_size
        for i in response:
            assert 'name' in i
            assert i['name'] is not None
            assert 'contract_address' in i
            assert i['contract_address'] is not None

            assert 'logo' in i
            assert 'href' in i

        print(response)
