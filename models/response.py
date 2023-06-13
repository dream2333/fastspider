import asyncio
from typing import Any, Coroutine, List, Optional, Self
from aiohttp import ClientResponse
from aiohttp.client import ClientSession
from aiohttp.client_reqrep import RequestInfo
from aiohttp.helpers import BaseTimerContext
from aiohttp.tracing import Trace
from aiohttp.typedefs import DEFAULT_JSON_DECODER, JSONDecoder
import orjson
from yarl import URL
from models import Request


class Response:
    @classmethod
    async def build(cls, request: Request, response: ClientResponse) -> None:
        obj = cls.__new__(cls)
        obj.url = response.url
        obj.raw_response = response
        obj.status = response.status
        obj.headers = response.headers
        obj.cookies = response.cookies
        obj.body = await response.read()
        obj.meta = request.meta
        obj.request = request
        obj._text = None
        obj._json = None
        obj._encoding = None
        return obj

    @property
    def text(self) -> str:
        if self._text is None:
            self._text = self.body.decode(self.encoding)
        return self._text

    @property
    def json(self) -> Any:
        if self._json is None:
            self._json = orjson.loads(self.body)
        return self._json

    @property
    def encoding(self) -> str:
        if self._encoding is None:
            self._encoding = self.raw_response.get_encoding()
        return self._encoding