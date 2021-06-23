#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: abstract_middleware
Description: 
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-23
"""
from abc import ABCMeta


class AbstractMiddleware(metaclass=ABCMeta):
    """抽象中间件类, RequestMiddleware 和 ResponseMiddleware 均继承自该类"""

    MIDDLEWARES = []  # 用于限制 middleware 注册顺序

    @property
    def middlewares(self):
        middlewares = self.MIDDLEWARES or [middleware for middleware in dir(self) if middleware.endswith("middleware")]
        return [getattr(self, middleware) for middleware in middlewares]
