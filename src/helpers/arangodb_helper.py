#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: arangodb_helper
Description: ArangoDB 异步客户端
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-18
"""
# !/usr/bin/env python
# -*- coding:utf-8 -*-

import asyncio

from conf import config
from helpers.abstract_helper import AbstractArangoDBClient
from utils import error_logger


class ArangoDBClient(AbstractArangoDBClient):

    def __init__(self, host: str, port: str, database: str, username: str, password: str, **kwargs):
        super().__init__(host, port, database, username, password, **kwargs)

    async def get_collections(self):
        try:
            return await self.client.collections()
        except Exception as e:
            error_logger.error("ArangoDBClient 客户端 get_collection 查询出错", exception=e)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    foo = loop.run_until_complete(ArangoDBClient(**config.ARANGO_CONFIG))
    print(loop.run_until_complete(foo.get_collections()))
    print(loop.run_until_complete(foo.client.close()))
