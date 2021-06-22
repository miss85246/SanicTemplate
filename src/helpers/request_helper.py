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
        self.bar = "bar"

    async def example_func(self):
        async with aiohttp.ClientSession() as session:
            resp = await session.get("http://httpbin.org/get", params={"foo": self.bar})
        return await resp.json()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    http_client = RequestClient()
    print(loop.run_until_complete(http_client.example_func()))
