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

from aioarangodb import ArangoClient

from utils import error_logger


class AbstractArangoDBClient:

    def __init__(self, host: str, port: str, database: str, username: str, password: str, **kwargs):
        self.client = None
        self._host = host
        self._port = port
        self._database = database
        self._username = username
        self._password = password

    async def __async_init__(self):
        client = ArangoClient(hosts=f"http://{self._host}:{self._port}")
        self.client = await client.db(name=self._database, username=self._username, password=self._password)
        return self

    def __await__(self):
        return self.__async_init__().__await__()


class ArangoDBClient(AbstractArangoDBClient):

    def __init__(self, host: str, port: str, database: str, username: str, password: str, **kwargs):
        super().__init__(host, port, database, username, password, **kwargs)

    async def get_collections(self):
        try:
            return await self.client.collections()
        except Exception as e:
            error_logger.error("ArangoDBClient 客户端 get_collection 查询出错", exception=e)


if __name__ == '__main__':
    info = {"host": "localhost", "port": "8529", "database": "example", "username": "root", "password": "datagrand"}
    loop = asyncio.get_event_loop()
    foo = loop.run_until_complete(ArangoDBClient(**info))
    print(loop.run_until_complete(foo.get_collections()))
