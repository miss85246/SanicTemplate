#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: response_middlewares
Description: 响应中间件
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-05-24
"""

from json import loads

from sanic.log import error_logger

from middlewares.abstract_middleware import AbstractMiddleware
from utils import json_response


class ResponseMiddleware(AbstractMiddleware):
    """
    返回中间件类, 主意执行顺序
    """
    MIDDLEWARES = []

    @staticmethod
    async def response_code_check_middleware(request, response):
        """检查返回结果代码中间件"""
        print(type(request), type(response))
        resp = loads(response.body)
        if resp.get("status", "FAILED") != "OK":
            error_msg = f"访问路由<{request.path}>失败, 请求方式:{request.method},"
            error_msg += f"请求参数:{request.body or request.args} \n \n[响应原文]:{response.body}"
            error_logger.error(error_msg)
            if resp.get("description"):
                return json_response(data={}, status_code=200, status=resp["description"])
