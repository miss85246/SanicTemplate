#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: es_helper
Description: elasticsearch 异步客户端
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-16
"""

from elasticsearch import AsyncElasticsearch


class EsClient:
    def __init__(self, host: str, port: str, username: str, password: str, **kwargs):
        self.client = AsyncElasticsearch([{"host": host, "port": port}], http_auth=(username, password), **kwargs)

    async def some_functions(self):
        body = {"query": {"match_all": {}}}
        res = await self.client.search(index="", doc_type="", body=body)
        return res
