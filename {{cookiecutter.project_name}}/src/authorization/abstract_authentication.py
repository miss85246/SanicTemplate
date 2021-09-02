# cookiecutter_flag {%- if cookiecutter.enable_jwt == 'True' %}
# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: abstract_authentication
Description: authentication 抽象类
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""

from abc import ABCMeta, abstractmethod

from sanic import Request


class AbstractAuthentication(metaclass=ABCMeta):
    """
    Authentication抽象类
    
    JWT 格式： header.payload.signature
    """

    def __init__(self):
        pass

    @abstractmethod
    async def authenticate(self, request: Request, *args, **kwargs):
        """
        JWT 验证函数

        :param request: Sanic 的 Request 对象
        :param args: 略
        :param kwargs: 略
        :return: 需要返回一个字典对象或具有 to_dict() 方法的类
        """
        pass

    @staticmethod
    async def payload_extender(payload: dict, user: dict, *args, **kwargs):
        """
        payload 字段拓展方法， 请注意不要放敏感信息

        :return: payload
        """
        payload.update({})
        return payload

    @staticmethod
    async def scopes_extender(user: dict, *args, **kwargs):
        """
        scope 权限拓展， 需要手动返回对应的用户权限列表，

        更多示例请查看：https://sanic-jwt.readthedocs.io/en/latest/pages/scoped.html#sample-code

        :return: 返回权限列表, example: ['user:read', 'admin', 'monitor:read:write']
        """
        pass
# cookiecutter_flag {%- endif %}
