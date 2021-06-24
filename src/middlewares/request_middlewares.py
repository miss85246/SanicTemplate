#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: request_middlewares
Description: 请求中间件类
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-05-24
"""

from sanic.log import logger

from middlewares.abstract_middleware import AbstractMiddleware


class RequestMiddleware(AbstractMiddleware):
    """请求中间件类, 注意顺序"""

    MIDDLEWARES = ['ab_middleware', 'test_middleware', 'ba_middleware']

    @staticmethod
    async def test_middleware(_):
        logger.info("a")

    @staticmethod
    async def ab_middleware(_):
        logger.info("b")

    @staticmethod
    async def ba_middleware(request):
        logger.info(dict(request.headers))
