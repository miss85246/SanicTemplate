#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: mongo_helper
Description: MongoDB 异步客户端
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-18
"""
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from conf import config
from utils import error_logger


class AbstractMongoClient:
    """抽象类, 封装了 MongoDB 初始化, 请勿在此类上进行修改"""

    def __init__(self, host: str, port: int, username: str = None, password: str = None, **kwargs):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = kwargs.get("database", None)
        self.collection = kwargs.get("collection", None)
        self.maxsize = kwargs.get("maxsize", 10)
        self.minsize = kwargs.get("minsize", 1)
        self.authSource = kwargs.get("authSource", "admin")
        self.timeout = kwargs.get("timeout", 10)
        self.uri = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.uri = self.uri + f"?authSource={self.authSource}"
        self.mongo = AsyncIOMotorClient(self.uri,
                                        maxPoolSize=self.maxsize,
                                        minPoolSize=self.minsize,
                                        waitQueueTimeoutMS=self.timeout)
        self.session = None

    async def __async__init__(self):
        self.database = self.mongo[self.database] if self.database else None
        self.collection = self.database[self.collection] if self.database and self.collection else None
        self.session = await self.mongo.start_session()
        return self

    def __await__(self):
        return self.__async__init__().__await__()


class MongoClient(AbstractMongoClient):

    def __init__(self, host: str, port: int, **kwargs):
        super().__init__(host, port, **kwargs)

    async def example_func(self):
        try:
            async with self.session.start_transaction():
                # await self.collection.insert_many([{"i": i} for i in range(2000)])
                cursor = self.collection.find({'i': {'$lt': 20}}).sort('i')
                return await cursor.to_list(length=10000)
        except Exception as e:
            error_logger.error("Mongo 查询 example_func 出错", exception=e)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    mongo_client = loop.run_until_complete(MongoClient(**config.MONGO_CONFIG))
    print(loop.run_until_complete(mongo_client.example_func()))
