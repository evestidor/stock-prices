import urllib.parse
from typing import List

import requests

from src.domain import Price

DEFAULT_HEADERS = {
    'Referer': 'https://br.tradingview.com/',
    'Origin': 'https://br.tradingview.com',
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.'
        '0.3770.100 Safari/537.36'
    ),
}


class B3Network:
    DOMAIN = 'https://scanner.tradingview.com/brazil/'

    def get(self, path: str):
        url = self._absolute_url(path)
        response = requests.get(url, headers=DEFAULT_HEADERS)
        return response.json()

    def post(self, path: str, data: dict = None):
        url = self._absolute_url(path)
        response = requests.post(url, json=data, headers=DEFAULT_HEADERS)
        return response.json()

    def _absolute_url(self, path: str) -> str:
        return urllib.parse.urljoin(self.DOMAIN, path)


class ListPricesOperation:

    def __init__(self, networking: B3Network):
        self._networking = networking

    def execute(self, symbols: List[str]) -> List[Price]:
        response = self._networking.post('scan', data={
            'symbols': {'tickers': symbols, 'query': {'types': []}},
            'columns': ['close'],
        })
        return self._parse_response(response)

    def _parse_response(self, response: List[dict]) -> List[Price]:
        return [Price(symbol=x['s'], amount=x['d']) for x in response['data']]


class ListSymbolsOperation:

    def __init__(self, networking: B3Network):
        self._networking = networking

    def execute(self) -> List[str]:
        response = self._networking.get('scan')
        return self._parse_response(response)

    def _parse_response(self, response) -> List[str]:
        return [x['s'] for x in response['data']]


class B3Facade:

    @staticmethod
    def list_prices(*symbols: List[str]) -> List[Price]:
        return ListPricesOperation(B3Network()).execute(symbols)

    @staticmethod
    def list_symbols() -> List[str]:
        return ListSymbolsOperation(B3Network()).execute()
