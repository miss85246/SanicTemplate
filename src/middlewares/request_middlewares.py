#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: request_middlewares
Description: 请求中间件
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-05-24
"""

from sanic.log import logger


class RequestMiddleware:
    """
    请求中间件类, 注意顺序, 执行顺序自上而下
    """

    @staticmethod
    async def test_middleware(request):
        logger.info(dict(request.headers))
