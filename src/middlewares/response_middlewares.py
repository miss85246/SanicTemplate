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

from utils import json_response
from sanic.log import error_logger


class ResponseMiddleware:
    """
    返回中间件类, 执行顺序自下而上
    """

    @staticmethod
    async def response_code_check_middleware(request, response):
        """
        检查返回结果代码中间件, 返回
        {'status': status, 'request_id': request_id, 'result_data': data or {}}
        :param request:
        :param response:
        """
        resp = loads(response.body)
        if resp.get("status", "FAILED") != "OK":
            error_logger.error(f"访问路由<{request.path}>失败, 请求方式:{request.method},请求参数:{request.body or request.args}"
                               + f"\n[响应原文]:{response.body}")
            if resp.get("description"):
                return json_response(data={}, status_code=200, status=resp["description"])
