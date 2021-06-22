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

from utils import error_logger
from conf import config


class RedisClient:
    """
    暂时只支持创建普通的 redis 连接池, 后期添加哨兵模式的支持
    """

    def __init__(self, host: str = None, port: str = None, password: str = None, mode="normal", **kwargs):
        self.redis = None
        self.kwargs = kwargs
        self.mode = mode
        self.nodes = kwargs.get("nodes", [(host, port)])
        self.node_size = len(self.nodes)
        self.password = None or password
        self.db = kwargs.pop("db", 0)
        self.timeout = kwargs.pop("timeout", 10)
        self.minsize = kwargs.pop("minsize", 1)
        self.maxsize = kwargs.pop("maxsize", 10)
        self.kwargs = kwargs

    async def redis_init(self):
        if self.redis is not None:
            raise ImportError("redis is already initialization")
        if self.mode == "normal":
            await self.redis_normal_client_init()

    async def redis_normal_client_init(self):
        self.redis = await aioredis.create_redis_pool(
            f"redis://{self.nodes[0][0]}:{self.nodes[0][1]}",
            db=self.db,
            password=self.password,
            maxsize=self.maxsize,
            minsize=self.minsize,
            timeout=self.timeout,
            **self.kwargs
        )

    async def example_test(self):

        try:
            await self.redis.set("zy_test", "123")
            res = await self.redis.get("zy_test")
            return res
        except Exception as e:
            error_logger.error(msg="执行 example_test 出错", exception=e)

    def __del__(self):
        self.redis.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    redis_cli = RedisClient(**config.REDIS_CONFIG)
    loop.run_until_complete(redis_cli.redis_init())
    print(loop.run_until_complete(redis_cli.example_test()))
    del redis_cli
    # loop.run_until_complete(redis_cli.redis.wait_closed())
