#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: request_middlewares
Description: 请求中间件类
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""

from middlewares.abstract_middleware import AbstractMiddleware


class RequestMiddleware(AbstractMiddleware):
    """请求中间件类, 注意顺序"""

    MIDDLEWARES = []
