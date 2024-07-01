from enum import Enum, auto
from common_fetch_strategy import ResponseType, Strategy
from pyodide.http import pyfetch, FetchResponse


class PyodideStrategy(Strategy):
    async def fetch(self, url, headers):
        response: FetchResponse = await pyfetch(
            url=url,
            method="GET",
            headers=headers,
        )
        if self.response_type == ResponseType.JSON:
            return await response.json()
        if self.response_type == ResponseType.BYTES:
            return await response.bytes()
