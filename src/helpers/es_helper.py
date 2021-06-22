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
from typing import Iterable

from elasticsearch import AsyncElasticsearch

from conf import config
from utils import error_logger


class AbstractEsClient:

    def __init__(self, host: str = None, port: str = None, username: str = "", password: str = "", **kwargs):
        if host and port and not kwargs.get("nodes"):
            self.nodes = [{"host": host, "port": port}]
        else:
            nodes = kwargs.get("nodes")
            if not isinstance(nodes, Iterable):
                raise TypeError("nodes argument must be Iterable, example: [{'host':'localhost', 'port':'9200'}]")
            for node in nodes:
                if not node.get("host") or not node.get("port"):
                    raise ValueError("host and port must in node")
            self.nodes = nodes
        self.client = None
        self.username = username
        self.password = password
        self.kwargs = kwargs

    async def __async__init__(self):
        self.client = AsyncElasticsearch(self.nodes, http_auth=(self.username, self.password), **self.kwargs)
        return self

    def __await__(self):
        return self.__async__init__().__await__()


class EsClient(AbstractEsClient):

    def __init__(self, host: str = None, port: str = None, username: str = "", password: str = "", **kwargs):
        super().__init__(host, port, username, password, **kwargs)

    async def example_functions(self):
        try:
            body = {"query": {"match_all": {}}}
            res = await self.client.search(index="logs-my_app-default", body=body, size=1)
            return res
        except Exception as e:
            error_logger.error("ESClient 查询 exception_function 出错", exception=e)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    es_client = loop.run_until_complete(EsClient(**config.ES_CONFIG))
    print(loop.run_until_complete(es_client.example_functions()))
