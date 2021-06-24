#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: es_helper
Description: elasticsearch 异步客户端
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-16
"""
import asyncio

from conf import config
from helpers.abstract_helper import AbstractEsClient
from utils import error_logger


class EsClient(AbstractEsClient):

    def __init__(self, host: str = None, port: str = None, username: str = "", password: str = "", **kwargs):
        super().__init__(host, port, username, password, **kwargs)

    async def example_func(self):
        try:
            body = {"query": {"match_all": {}}}
            res = await self.client.search(index="logs-my_app-default", body=body, size=1)
            return res
        except Exception as e:
            error_logger.error("ESClient 查询 exception_function 出错", exception=e)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    es_client = loop.run_until_complete(EsClient(**config.ES_CONFIG))
    print(loop.run_until_complete(es_client.example_func()))
    loop.run_until_complete(es_client.close())
