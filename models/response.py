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


class Response(ClientResponse):
    def __init__(self, response:ClientResponse) -> None:
        self.__dict__ = response.__dict__

    async def json(
        self, *, encoding: str | None = None, loads: JSONDecoder = orjson.loads, content_type: str | None = None
    ) -> Coroutine[Any, Any, Any]:
        return await super().json(encoding=encoding, loads=loads, content_type=content_type)
