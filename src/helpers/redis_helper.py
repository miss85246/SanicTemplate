#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: redis_helper
Description: Redis 异步客户端, 使用 aioredis 1.3.1+ 版本
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-18
"""
import asyncio

import aioredis

from conf import config
from utils import error_logger


class AbstractRedisClient:

    def __init__(self, host: str = None, port: str = None, password: str = None, mode: str = "normal", **kwargs):
        self.redis = None
        self.kwargs = kwargs
        self.mode = mode
        self.nodes = kwargs.get("nodes", [(host, port)])
        self.node_size = len(self.nodes)
        self.password = None or password
        self.database = kwargs.pop("database", 0)
        self.timeout = kwargs.pop("timeout", 10)
        self.minsize = kwargs.pop("minsize", 1)
        self.maxsize = kwargs.pop("maxsize", 10)
        self.kwargs = kwargs

    async def __async__init__(self):
        self.redis = await aioredis.create_redis_pool(f"redis://{self.nodes[0][0]}:{self.nodes[0][1]}",
                                                      db=self.database,
                                                      password=self.password,
                                                      maxsize=self.maxsize,
                                                      minsize=self.minsize,
                                                      timeout=self.timeout,
                                                      **self.kwargs)
        return self

    def __await__(self):
        return self.__async__init__().__await__()

    def __del__(self):
        self.redis.close()


class RedisClient(AbstractRedisClient):

    def __init__(self, host: str = None, port: str = None, password: str = None, mode: str = "normal", **kwargs):
        super().__init__(host, port, password, mode, **kwargs)

    async def example_test(self):
        try:
            await self.redis.set("sanic_test", "123")
            res = await self.redis.get("sanic_test")
            return res
        except Exception as e:
            error_logger.error(msg="执行 example_test 出错", exception=e)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    redis_cli = loop.run_until_complete(RedisClient(**config.REDIS_CONFIG))
    print(loop.run_until_complete(redis_cli.example_test()))
    del redis_cli
