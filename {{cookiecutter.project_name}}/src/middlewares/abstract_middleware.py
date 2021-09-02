#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: abstract_middleware
Description: 抽象中间件类，请求中间件与响应中间件类都继承于此
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""
from abc import ABCMeta


class AbstractMiddleware(metaclass=ABCMeta):
    """抽象中间件类, RequestMiddleware 和 ResponseMiddleware 均继承自该类"""

    MIDDLEWARES = []  # 用于限制 middleware 注册顺序

    @property
    def middlewares(self):
        """
        获取中间件，可以用作属性使用

        :return:
        """
        middlewares = self.MIDDLEWARES or [middleware for middleware in dir(self) if middleware.endswith("middleware")]
        return [getattr(self, middleware) for middleware in middlewares]
