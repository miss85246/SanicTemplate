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
from elasticsearch import AsyncElasticsearch
from conf import config


class EsClient:
    def __init__(self, nodes: list = None, host: str = "", port: str = "", username: str = "",
                 password: str = "", **kwargs):

        if host and port:
            self.nodes = [{"host": host, "port": port}]
        else:
            for node in nodes:
                if not node.get("host") or not node.get("port"):
                    raise ValueError("host and port must in node")
            self.nodes = nodes
        self.client = AsyncElasticsearch(self.nodes, http_auth=(username, password), **kwargs)

    async def example_functions(self):
        body = {"query": {"match_all": {}}}
        res = await self.client.search(index="logs-my_app-default",  body=body, size=1)
        return res


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    es_client = EsClient(**config.ES_CONFIG)
    print(loop.run_until_complete(es_client.example_functions()))
