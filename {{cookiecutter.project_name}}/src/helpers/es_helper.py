# cookiecutter_flag {%- if cookiecutter.enable_elasticsearch == 'True' %}
# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: es_helper
Description: elasticsearch 异步客户端
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""
import asyncio

from conf import config
from helpers.abstract_helper import AbstractEsClient
from utils import error_logger


class EsClient(AbstractEsClient):

    def __init__(self, nodes: [str], username: str = "", password: str = "", **kwargs):
        super().__init__(nodes, username, password, **kwargs)

    async def example_func(self):
        try:
            body = {"query": {"match_all": {}}}
            res = await self.client.search(index="logs-my_app-default", body=body, size=1)
            return res
        except Exception as e:
            error_logger.error("ESClient 查询 exception_function 出错", exception=e)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    es_client = loop.run_until_complete(EsClient(**config.ES_CONFIG))
    print(loop.run_until_complete(es_client.example_func()))
    loop.run_until_complete(es_client.close())
# cookiecutter_flag {%- endif %}
