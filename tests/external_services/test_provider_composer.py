from src.external_services import ProviderComposer
from src.modules.nft.domain.collection import Collection


class TestProviderComposer:
    def test_fetch_collection(self):
        bored_ape_contract_address =\
            '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'
        client = ProviderComposer()
        collection = client.fetch_collection(bored_ape_contract_address)

        assert isinstance(collection, Collection)
        assert collection.symbol == 'BAYC'
        assert collection.type.value == 'ERC721'
        assert collection.name == 'BoredApeYachtClub'
        assert collection.contract_address ==\
            bored_ape_contract_address.lower()

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
