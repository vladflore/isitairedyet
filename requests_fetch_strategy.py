import aiohttp
import requests

from common_fetch_strategy import Strategy


class RequestsStrategy(Strategy):
    async def fetch(self, url, headers):
        response = requests.get(url, headers=headers)
        return response.json()


class AIOHttpStrategy(Strategy):
    async def fetch(self, url, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()
