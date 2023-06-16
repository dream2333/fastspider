from typing import Any, Optional, Self, List
from aiohttp import ClientResponse
import orjson
from models import Request
from parsel import Selector, SelectorList
from utils import lazy_porperty


class Response:
    __slots__ = (
        "raw_response",
        "status",
        "headers",
        "cookies",
        "content",
        "meta",
        "request",
    )

    @classmethod
    async def build(cls, request: Request, response: ClientResponse) -> Self:
        """
        从给定的请求和响应构建Response对象。

        Args:
            request (Request): 请求对象。
            response (ClientResponse): 响应对象。

        Returns:
            Self: 构建的Response对象。
        """
        obj = cls.__new__(cls)
        obj.raw_response = response
        obj.status = response.status
        obj.headers = response.headers
        obj.cookies = response.cookies
        obj.content = await response.read()
        obj.meta = request.meta
        obj.request = request
        return obj

    @lazy_porperty
    def url(self) -> str:
        return self.raw_response.url.human_repr()

    @lazy_porperty
    def text(self) -> str:
        return self.content.decode(self.encoding)

    @lazy_porperty
    def json(self) -> Any:
        return orjson.loads(self.text)

    @lazy_porperty
    def encoding(self) -> str:
        return self.raw_response.get_encoding()

    @lazy_porperty
    def selector(self) -> Selector:
        return Selector(text=self.text)

    def xpath(self, query: str, url: Optional[str] = None) -> SelectorList[Selector]:
        """
        返回匹配给定XPath查询的Selector对象列表。

        Args:
            query (str): 要匹配的XPath查询。
            url (Optional[str]): 用于解析XPath查询中的相对URL的URL。

        Returns:
            SelectorList[Selector]: 匹配给定XPath查询的Selector对象列表。
        """
        return self.selector.xpath(query, url=url)

    def re(self, query: str, replace_entities: bool = True) -> List[str]:
        """
        返回匹配给定正则表达式的字符串列表。

        Args:
            query (str): 要匹配的正则表达式。
            replace_entities (bool): 是否替换HTML实体。

        Returns:
            List[str]: 匹配给定正则表达式的字符串列表。
        """
        return self.selector.re(query, replace_entities)

    def re_first(self, query: str, replace_entities: bool = True) -> List[str]:
        """
        返回匹配给定正则表达式的第一个字符串。

        Args:
            query (str): 要匹配的正则表达式。
            replace_entities (bool): 是否替换HTML实体。

        Returns:
            List[str]: 匹配给定正则表达式的第一个字符串。
        """
        return self.selector.re(query, replace_entities)[:1]
