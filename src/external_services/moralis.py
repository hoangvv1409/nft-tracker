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
