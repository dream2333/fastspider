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
    __slots__ = (
        "url",
        "raw_response",
        "status",
        "headers",
        "cookies",
        "body",
        "meta",
        "request",
        "__text",
        "__json",
        "__encoding",
    )

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
        obj.__text = None
        obj.__json = None
        obj.__encoding = None
        return obj

    @property
    def text(self) -> str:
        if self.__text is None:
            self.__text = self.body.decode(self.encoding)
        return self.__text

    @property
    def json(self) -> Any:
        if self.__json is None:
            self.__json = orjson.loads(self.text)
        return self.__json

    @property
    def encoding(self) -> str:
        if self.__encoding is None:
            self.__encoding = self.raw_response.get_encoding()
        return self.__encoding
