#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: entity_related_doc
Description: 通过实体获取相关联的文档信息
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-05-24
"""

from sanic.log import error_logger
from sanic.views import HTTPMethodView
from sanic_dantic import parse_params

from models import TestDanticModel
from utils import json_response


class TestView(HTTPMethodView):
    decorators = [parse_params(body=TestDanticModel)]

    async def post(self, request, params):
        """
        POST 请求
        :param request: 请求对象
        :param params: {entity:实体名称}
        :return:
        """

        # 从读取的内容中提取相关联的文档信息
        try:
            db_result = await request.app.ctx.database.example_func(filter_id=params.test)
            es_result = await request.app.ctx.es.example_func()
            redis_result = await request.app.ctx.redis.example_func()
            arango_result = await request.app.ctx.arangodb.example_func()
            request_result = await request.app.ctx.request.example_func()
            assert db_result and es_result and redis_result
        except AssertionError as e:
            error_logger.error(msg="查询失败,没有返回结果", exception=e)
            return json_response(data={}, status_code=200, status="Not Found")
        except Exception as e:
            error_logger.error("TestView异常报错", exception=e)
            return json_response(data={}, status_code=500, status="Failed")
        result_data = {
            "test": params.test,
            "db_result": db_result,
            "es_result": es_result,
            "redis_result": redis_result,
            "request_result": request_result,
            "arango_result": arango_result
        }
        return json_response(data=result_data, status_code=200, status="OK")
