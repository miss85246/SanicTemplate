# cookiecutter_flag {%- if cookiecutter.enable_redis == 'True' %}
# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: redis_helper
Description: Redis 异步客户端, 使用 aioredis 1.3.1+ 版本
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""
import asyncio

from conf import config
from helpers.abstract_helper import AbstractRedisClient
from utils import error_logger


class RedisClient(AbstractRedisClient):

    def __init__(self, host: str = None, port: int = None, password: str = None, mode: str = "normal", **kwargs):
        super().__init__(host, port, password, mode, **kwargs)

    async def example_func(self):
        try:
            await self.redis.set("sanic_test", "123")
            res = await self.redis.get("sanic_test")
            return res
        except Exception as e:
            error_logger.error(msg="执行 example_test 出错", exception=e)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    redis_cli = loop.run_until_complete(RedisClient(**config.REDIS_CONFIG))
    print(loop.run_until_complete(redis_cli.example_func()))
    loop.run_until_complete(redis_cli.close())
# cookiecutter_flag {%- endif %}
