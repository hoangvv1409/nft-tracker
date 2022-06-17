import requests
from typing import Dict

from .base import BaseClient

DEFAULT_CHAIN = 'eth'


class Moralis(BaseClient):
    def __init__(self, base_url, api_key):
        super().__init__()
        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-API-Key': api_key,
        }

    def get_collection_metadata(
        self, contract_address: str, chain: str = DEFAULT_CHAIN,
    ) -> Dict:
        url = f'{self.base_url}/nft/{contract_address}/metadata?chain={chain}'
        response = self.response_handler(requests.get, {
            'url': url,
            'headers': self.headers
        })

        return response.json()

    def get_trade_activity_of_collection(
        self, contract_address: str, limit: int = 50,
        from_date: str = None, to_date: str = None,
        cursor: str = None,
    ):
        url = f'{self.base_url}/nft/{contract_address}/trades?limit={limit}'
        if from_date:
            url = f'{url}&from_date={from_date}'
        if to_date:
            url = f'{url}&to_date={to_date}'
        if cursor:
            url = f'{url}&cursor={cursor}'

        response = self.response_handler(requests.get, {
            'url': url,
            'headers': self.headers,
        })

        return response.json()

    def get_erc20_metadata(self, contract_address: str):
        url = f'{self.base_url}/erc20/metadata?chain=eth'
        url = f'{url}&addresses={contract_address}'

        response = self.response_handler(requests.get, {
            'url': url,
            'headers': self.headers,
        })

        return response.json()
