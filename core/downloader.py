import aiohttp
import orjson


def serializer(jsonstr):
    return orjson.dumps(jsonstr).decode()


class Downloader:
    def __init__(self) -> None:
        self.client = aiohttp.ClientSession(json_serialize=serializer)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.close()
        if exc:
            print(exc_type, exc, tb)

    async def request(self, url, method="GET", verify_ssl=False, **kwargs):
        async with aiohttp.request(method, url, verify_ssl=verify_ssl, **kwargs) as response:
            return await response.text()

    async def request_with_session(self, url, method="GET", verify_ssl=False, **kwargs):
        response = await self.client.request(method, url, verify_ssl=verify_ssl, **kwargs)
        return response
