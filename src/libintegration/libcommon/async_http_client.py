import aiohttp
import logging

class AsyncHTTPClient:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    async def _make_request(self, method, endpoint, data=None, headers=None):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, f"{self.base_url}{endpoint}", data=data, headers=headers, timeout=self.timeout) as response:
                    response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
                    return response
            except aiohttp.ClientError as client_err:
                self.logger.error(f'Client error occurred: {client_err}')
                raise
            except Exception as err:
                self.logger.error(f'An error occurred: {err}')
                raise

    async def get(self, endpoint, headers=None):
        return await self._make_request('GET', endpoint, headers=headers)

    async def post(self, endpoint, data, headers=None):
        return await self._make_request('POST', endpoint, data=data, headers=headers)

    async def patch(self, endpoint, data, headers=None):
        return await self._make_request('PATCH', endpoint, data=data, headers=headers)

    async def delete(self, endpoint, headers=None):
        return await self._make_request('DELETE', endpoint, headers=headers)
