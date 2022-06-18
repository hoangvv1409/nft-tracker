from src.external_services import ProviderComposer
from src.modules.nft.domain import (
    Collection, Erc20, CollectionTransaction)


bored_ape_contract_address =\
    '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'
erc20_usdc_contract_address = \
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
non_exist_contract_address = \
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb43'


class TestProviderComposer:
    def test_fetch_collection(self):
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

    def test_fetch_erc20_metadata(self):
        client = ProviderComposer()
        erc20 = client.fetch_erc20(erc20_usdc_contract_address)

        assert isinstance(erc20, Erc20)

    def test_fetch_erc20_metadata_with_non_exist_contract(self):
        client = ProviderComposer()
        erc20 = client.fetch_erc20(non_exist_contract_address)

        assert erc20 is None

    def test_fetch_collection_transfer_activity(self):
        client = ProviderComposer()
        txn_gen = client.fetch_collection_transfer_activity(
            bored_ape_contract_address)

        for txn, next_cursor in txn_gen:
            assert isinstance(txn, CollectionTransaction)
            assert next_cursor is not None

    def test_fetch_collection_transfer_activity_with_date_range(self):
        client = ProviderComposer()
        txn_gen = client.fetch_collection_transfer_activity(
            contract_address=bored_ape_contract_address,
            from_date='2022-06-15T00:00:00.000Z',
            to_date='2022-06-15T23:59:59.000Z',
        )

        for txn, next_cursor in txn_gen:
            assert isinstance(txn, CollectionTransaction)
            assert next_cursor is None
