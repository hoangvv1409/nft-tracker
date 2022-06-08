import requests
from typing import Dict, List
from bs4 import BeautifulSoup


class EtherScanScraper():
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'PostmanRuntime/7.29.0',
            'Accept': '*/*',
        }

    def get_all_collections(
        self, page: int = 1, page_size: int = 100,
    ) -> List[Dict]:
        url = f'{self.base_url}/tokens-nft?ps={page_size}&p={page}'
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find(id='content')

        collections = []
        items = results.find_all('div', class_='media')
        for i in items:
            a_tag = i.find('a')
            logo = i.find('img')['src']
            if 'empty-token.png' in logo:
                logo = None
            else:
                logo = f'{self.base_url}/{logo}'

            contract_address = a_tag.get('title')
            if not contract_address:
                continue

            collections.append({
                'name': a_tag.text.strip(),
                'contract_address': contract_address,
                'logo': logo,
                'href': a_tag['href'],
            })

        return collections
