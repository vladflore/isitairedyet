from abc import ABC, abstractmethod
from enum import Enum, auto


class ResponseType(Enum):
    JSON = auto()
    BYTES = auto()


class Strategy(ABC):
    response_type: ResponseType = ResponseType.JSON
    
    @abstractmethod
    def fetch(self, url, headers):
        pass


class FetchData:
    def __init__(self, url: str, headers, strategy: Strategy) -> None:
        self._url = url
        self._headers = headers
        self._strategy = strategy

    async def fetch(self):
        return await self._strategy.fetch(self._url, self._headers)
