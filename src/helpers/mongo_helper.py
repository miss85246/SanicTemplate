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

from conf import config
from helpers.abstract_helper import AbstractMongoClient
from utils import error_logger


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
    loop.run_until_complete(mongo_client.close())
