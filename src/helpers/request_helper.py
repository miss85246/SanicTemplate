#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: request_handler
Description: Request 异步客户端
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-21
"""
import asyncio
import aiohttp


class RequestClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def example_func(self):
        resp = await self.session.get("https://httpbin.org/get", params={"foo": "bar"})
        return await resp.json()


if __name__ == '__main__':
    http_client = RequestClient()
    loop = asyncio.get_event_loop()

    print(loop.run_until_complete(http_client.example_func()))
    loop.run_until_complete(http_client.session.close())
