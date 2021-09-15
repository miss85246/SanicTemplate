# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: request_handler
Description: Request 异步客户端
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2021-09-08
"""
import asyncio

from helpers.abstract_helper import AbstractHttpxClient
from utils import timer


class HttpxClient(AbstractHttpxClient):

    def __init__(self):
        super().__init__(timeout=10, retry=5, status_retry=True)
        self.session.headers.update({"User-Agent": "Sanic HttpClient Test"})

    @timer()
    async def example_func(self):
        resp = await self.post("https://httpbin.org/post", json={"foo": "bar"})
        return resp.json()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = loop.run_until_complete(HttpxClient())
    res = loop.run_until_complete(client.example_func())
    print(res)
    loop.run_until_complete(client.close())
