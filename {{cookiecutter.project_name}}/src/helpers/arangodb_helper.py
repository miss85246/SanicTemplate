# cookiecutter_flag {%- if cookiecutter.enable_arangodb == 'True' %}
# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: arangodb_helper
Description: ArangoDB 异步客户端
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""
# !/usr/bin/env python
# -*- coding:utf-8 -*-

import asyncio

from conf import config
from helpers.abstract_helper import AbstractArangoDBClient
from utils import error_logger


class ArangoDBClient(AbstractArangoDBClient):

    def __init__(self, hosts: str, database: str, username: str, password: str, host_resolver: str):
        super().__init__(hosts, database, username, password, host_resolver)

    async def example_func(self):
        try:
            cursor = await self.client.aql.execute("for user in test return user")
            return [item async for item in cursor]
        except Exception as e:
            error_logger.error("ArangoDBClient 客户端 get_collection 查询出错", exception=e)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    foo = loop.run_until_complete(ArangoDBClient(**config.ARANGO_CONFIG))
    print(loop.run_until_complete(foo.example_func()))
    loop.run_until_complete(foo.close())
# cookiecutter_flag {%- endif %}
