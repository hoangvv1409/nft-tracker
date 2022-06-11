from src.external_services import ProviderComposer
from src.modules.nft.domain.collection import Collection


class TestProviderComposer:
    def test_fetch_collections(self):
        page_size = 10
        client = ProviderComposer()
        # test with small page_size (10) for faster result
        response = client.fetch_collections(page=1, page_size=page_size)

        assert len(response) == page_size

    def test_fetch_collections_iterator(self):
        page_size = 10
        loop_count = 0
        client = ProviderComposer()

        fetch_collections_gen = client.fetch_collections_iterator(
            page=1, page_size=page_size)

        for collection in fetch_collections_gen:
            assert isinstance(collection, Collection)
            loop_count += 1

        assert loop_count == page_size
