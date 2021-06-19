#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: response
Description: 自定义 response 返回格式
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-05-24
"""

from time import time
from json import loads, dumps
from sanic.response import json


def json_response(data: dict = None, status_code: int = 200, status: str = "OK"):
    """
    封装 json 返回方式
    :param data: 要返回的内容
    :param status_code: 响应状态码
    :param status: 响应状态
    :return:
    """
    request_id = time() * 1000000
    response = {
        "request_id": request_id,
        "result_data": loads(dumps(data or {}, default=str, ensure_ascii=True)),
        "status": status
    }
    return json(response, status=status_code)
