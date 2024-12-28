import requests
import logging

from settings import settings

class HTTPClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    def _make_request(self, method, endpoint, data=None, headers=None):
        try:
            response = requests.request(
                method, f"{self.base_url}{endpoint}", data=data, headers=headers, timeout=settings.TIMEOUT
            )
            response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
            return response
        except requests.exceptions.HTTPError as http_err:
            self.logger.info(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            self.logger.info(f'An error occurred: {err}')
            raise

    def get(self, endpoint, headers=None):
        return self._make_request('GET', endpoint, headers=headers)

    def post(self, endpoint, data, headers=None):
        return self._make_request('POST', endpoint, data=data, headers=headers)

    def patch(self, endpoint, data, headers=None):
        return self._make_request('PATCH', endpoint, data=data, headers=headers)

    def delete(self, endpoint, headers=None):
        return self._make_request('DELETE', endpoint, headers=headers)
