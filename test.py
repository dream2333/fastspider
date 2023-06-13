import asyncio
import aiohttp
async def fetch(session, url):
    # with语句保证在处理session的时候，总是能正确的关闭它
    async with session.get(url) as resp:
        # 1.如果想要得到结果，则必须使用await关键字等待请求结束，如果没有await关键字，得到的是一个生成器
        # 2.text()返回的是字符串的文本，read()返回的是二进制的文本
        data = await resp.text()
        print('data', data)
        return data


async def run():
    async with aiohttp.ClientSession() as session:
        html_data = await fetch(session, "http://127.0.0.1:5000/")
        print('html', html_data)


if __name__ == '__main__':
    asyncio.run(run())