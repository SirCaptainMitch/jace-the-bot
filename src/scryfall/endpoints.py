import ujson as json
from pydantic import BaseModel, Field
# import requests as req
import httpx as req
from src.scryfall.config import BASE_URI
# from scryfall.exceptions import APIException, AuthenticationError


class APIClient(BaseModel):

    base_url: str = Field(default=BASE_URI)

    @staticmethod
    def build_headers(headers=None) -> dict:

        if headers:
            headers = {
                'Content-Type': 'application/json',
                **headers
            }
            return headers

        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/json',
        }
        return headers

    def request(self, url: str, method: str | None = 'GET', params=None, data=None, headers=None) -> req.Response:

        headers = self.build_headers(headers)
        response = req.request(
            url
            , method
            , params=params
            , json=data
            , headers=headers
            , timeout=500.00
        )
        # if response.status_code == 401:
        #     raise AuthenticationError('Invalid authentication token.')
        # if response.status_code >= 400:
        #     raise APIException(f'Error {response.status_code}: {response.text}')
        return response


class BulkEndpoint(APIClient):
    base_endpoint: str = Field(default='/bulk-data')

    def get_bulk_data(self) -> list[str]:
        endpoint = f'{self.base_endpoint}'
        url = f'{self.base_url}/{endpoint}'
        data = self.request('GET', url)
        return data.json().get('data')

    def get_oracle_cards(self):
        endpoint = f'{self.base_endpoint}/oracle-cards'
        url = f'{self.base_url}/{endpoint}'
        res = self.request('GET', url).json()
        data = self.request('GET', res['download_uri'], headers={
            'Accept-Encoding': 'gzip'
        }).content
        return json.loads(data)

    def get_rulings(self):
        endpoint: str = f'{self.base_endpoint}/rulings'
        url = f'{self.base_url}/{endpoint}'
        res = self.request('GET', url).json()
        data = self.request('GET', res['download_uri'], headers={
            'Accept-Encoding': 'gzip'
        }).content
        return json.loads(data)

    def get_all_cards(self):
        endpoint: str = f'{self.base_endpoint}/all-cards'
        url = f'{self.base_url}/{endpoint}'
        res = self.request('GET', url).json()
        data = self.request('GET', res['download_uri'], headers={
            'Accept-Encoding': 'gzip'
        }).content
        return json.loads(data)

    def get_unique_artwork(self):
        endpoint: str = f'{self.base_endpoint}/unique-artwork'
        url = f'{self.base_url}/{endpoint}'
        res = self.request('GET', url).json()
        data = self.request('GET', res['download_uri'], headers={
            'Accept-Encoding': 'gzip'
        }).content
        return json.loads(data)

    def get_default_cards(self):
        endpoint: str = f'{self.base_endpoint}/default-cards'
        url = f'{self.base_url}/{endpoint}'
        res = self.request('GET', url).json()
        data = self.request('GET', res['download_uri'], headers={
            'Accept-Encoding': 'gzip'
        }).content
        return json.loads(data)


class CatalogEndpoint(APIClient):
    base_endpoint: str = Field(default='/catalog')

    def get_catalog(self, name: str) -> list[str]:
        endpoint = f'{self.base_endpoint}/{name}'
        url = f'{self.base_url}/{endpoint}'
        data = self.request('GET', url)
        return data.json().get('data')

    def get_catalog_response(self, name: str) -> req.Response:
        endpoint = f'{self.base_endpoint}/{name}'
        url = f'{self.base_url}/{endpoint}'
        res = self.request('GET', url)
        return res


