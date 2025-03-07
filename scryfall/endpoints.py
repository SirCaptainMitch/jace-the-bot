from abc import ABC, abstractmethod

import httpx as req
import ujson as json
from pydantic import BaseModel, Field

from scryfall.config import BASE_URI


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


class Endpoint(ABC):

    @abstractmethod
    def _resolve_url(self):
        """Resolves the URL to ensure it is properly formatted."""

    @abstractmethod
    def get(self):
        """Interface for a Rest GET endpoint."""


class DataEndpoint(Endpoint, APIClient):
    base_endpoint: str = Field(default=None)

    def _resolve_url(self):
        print(self.base_url)
        return f'{self.base_url}/{self.base_endpoint}'

    def get(self):
        """Gets Scryfall data from the API that does not require a full file download."""
        url = self._resolve_url()
        data = self.request('GET', url)
        return data.json().get('data')


class BulkDataEndpoint(Endpoint, APIClient):
    bulk_endpoint: str = Field(default='/bulk-data')
    base_endpoint: str = Field(default=None)
    headers: dict = Field(default={'Accept-Encoding': 'gzip'})

    def _resolve_url(self):
        return f'{self.base_url}/{self.bulk_endpoint}/{self.base_endpoint}'

    def get(self) -> dict:
        url = self._resolve_url()
        res = self.request('GET', url).json()
        data = self.request('GET', res['download_uri'], headers=self.headers).content
        return json.loads(data)


class OracleCardEndpoint(BulkDataEndpoint):
    base_endpoint: str = Field(default='/oracle-cards')

    def get(self):
        """Gets the Oracle Cards data from Scryfall by downloading the bulk file.
        This file name changes daily, and requires two calls to get the correct uri.
        """
        return super().get()


class RulingEndpoint(BulkDataEndpoint):
    base_endpoint: str = Field(default='/rulings')

    def get(self):
        """Gets the Card Ruling data from Scryfall by downloading the bulk file.
        This file name changes daily, and requires two calls to get the correct uri.
        """
        return super().get()


class AllCardsEndpoint(BulkDataEndpoint):
    base_endpoint: str = Field(default='/all-cards')

    def get(self):
        """Gets the All Cards data from Scryfall by downloading the bulk file.
        This file name changes daily, and requires two calls to get the correct uri.
        """
        return super().get()


class UniqueArtworkEndpoint(BulkDataEndpoint):
    base_endpoint: str = Field(default='/unique-artwork')

    def get(self):
        """Gets the Unique Artwork for cards data from Scryfall by downloading the bulk file.
        This file name changes daily, and requires two calls to get the correct uri.
        """
        return super().get()


class DefaultCardEndpoint(BulkDataEndpoint):
    base_endpoint: str = Field(default='/default-cards')

    def get(self):
        """Gets the Oracle Cards data from Scryfall by downloading the bulk file.
        This file name changes daily, and requires two calls to get the correct uri.
        """
        return super().get()


class CatalogEndpoint(DataEndpoint):
    catalog_name: str = Field(default=None)
    base_endpoint: str = Field(default='/catalog')

    def _resolve_url(self):
        return f'{self.base_url}/{self.base_endpoint}/{self.catalog_name}'

    def get(self) -> list[str]:
        """Gets data from the Scryfall API for a specific catalog."""
        return super().get()


class SetEndpoint(DataEndpoint):
    base_endpoint: str = Field(default='/sets')

    def get(self) -> list[str]:
        """Gets data from the Scryfall API for all sets."""
        return super().get()


if __name__ == '__main__':
    pass
