from src.external_services import ProviderComposer


class TestProviderComposer:
    def test_get_all_collections(self):
        client = ProviderComposer()
        # test with small page_size (10) for faster result
        response = client.fetch_collections(page=1, page_size=10)

        assert len(response) == 10
