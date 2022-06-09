import requests
from typing import List, Dict

from .base import BaseClient


class OpenSea(BaseClient):
    def __init__(self, base_url, api_key):
        super().__init__()
        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-API-KEY': api_key,
        }

    def get_all_collections(
        self, page: int = 1, page_size: int = 100,
    ) -> List[Dict]:
        pass

    def get_collection_metadata(self, contract_address: str) -> Dict:
        url = f'{self.base_url}/asset_contract/{contract_address}'
        response = self.response_handler(requests.get, {
            'url': url,
            'headers': self.headers,
        })

        return response.json()

    def get_collection_stats(self, slug: str) -> Dict:
        url = f'{self.base_url}/collection/{slug}/stats'
        response = self.response_handler(requests.get, {
            'url': url,
            'headers': self.headers,
        })

        return response.json()
