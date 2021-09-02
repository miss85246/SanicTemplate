#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: entity_related_doc
Description: 测试视图
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""

from sanic.views import HTTPMethodView
from sanic_dantic import parse_params
# cookiecutter_flag {%- if cookiecutter.enable_jwt == 'True' %}
from sanic_jwt import protected

# cookiecutter_flag {%- endif %}
from models import TestDanticModel
from utils import json_response


class TestView(HTTPMethodView):
    decorators = [
        parse_params(body=TestDanticModel),
        # cookiecutter_flag {%- if cookiecutter.enable_jwt == 'True' %}
        protected()
        # cookiecutter_flag {%- endif %}
    ]

    async def post(self, request, params):
        """
        POST 请求
        :param request: 请求对象
        :param params: {entity:实体名称}
        :return:
        """
        return json_response(data={"foo": "bar"}, status_code=200, status="OK")
