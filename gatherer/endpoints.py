import json
from pydantic import BaseModel, Field
import requests as req
from gatherer.config import BASE_URI, CURRENT_RULE_URI
# from scryfall.exceptions import APIException, AuthenticationError


class APIClient(BaseModel):

    base_url: str = Field(default=BASE_URI)

    @staticmethod
    def request(method, url, params=None, data=None, headers=None):
        if headers:
            headers = {
                'Content-Type': 'text/plain',
                **headers
            }
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'text/plain',
            }

        response = req.request(method, url, params=params, json=data, headers=headers)

        # if response.status_code == 401:
        #     raise AuthenticationError('Invalid authentication token.')
        # if response.status_code >= 400:
        #     raise APIException(f'Error {response.status_code}: {response.text}')
        return response.content


class RulesEndpoint(APIClient):

    def get_txt_rules(self):
        url = f'{CURRENT_RULE_URI}'
        data = self.request('GET', url)
        return data
