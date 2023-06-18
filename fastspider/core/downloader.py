import aiohttp
import orjson
from fastspider.models import Request, Response


def serializer(jsonstr):
    return orjson.dumps(jsonstr).decode()


class Downloader:
    def __init__(self) -> None:
        self.client = aiohttp.ClientSession(json_serialize=serializer, read_bufsize=2**18)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        await self.client.close()

    async def request(self, url, method="GET", verify_ssl=False, **kwargs):
        async with aiohttp.request(method, url, verify_ssl=verify_ssl, **kwargs) as response:
            return await response.text()

    # url: str
    # callback: str = None
    # method = "GET"
    # params: dict = None
    # headers: dict = None
    # cookies: dict = None
    # json: dict = None
    # data: bytes | str = None
    # verify_ssl: bool = False
    # meta: dict = None
    # errback: str = None
    # kwargs: dict = None

    async def request_with_session(self, request: Request):
        response = await self.client.request(
            request.method,
            url=request.url,
            params=request.params,
            data=request.data,
            headers=request.headers,
            cookies=request.cookies,
            json=request.json,
            verify_ssl=request.verify_ssl,
            **request.req_kwargs
        )
        return await Response.build(request, response)
