#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: server.py
Description: Server 文件, 用于启动服务
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-04-28
"""

from sanic import Sanic
from conf import config
from middlewares import RequestMiddleware, ResponseMiddleware
from route import server_bp
from helpers import DBClient, EsClient, RedisClient, RequestClient

server_app = Sanic("server", log_config=config.LOGGING_CONFIG)
server_app.config.update_config(config)
server_app.blueprint(server_bp)


@server_app.listener("after_server_start")
async def server_init(_, __):
    """用于初始化挂载存储中间件"""
    server_app.ctx.db = DBClient(**server_app.config.DB_CONFIG)
    await server_app.ctx.db.session_init()
    server_app.ctx.es = EsClient(**server_app.config.ES_CONFIG)
    server_app.ctx.redis = RedisClient(**server_app.config.REDIS_CONFIG)
    await server_app.ctx.redis.redis_init()
    server_app.ctx.request = RequestClient()


@server_app.listener("after_server_start")
async def register_request_middleware(_, __):
    """注册请求中间件"""
    for middleware in [func for func in dir(RequestMiddleware) if func.endswith("middleware")]:
        server_app.register_middleware(getattr(RequestMiddleware, middleware), "request")


@server_app.listener("after_server_start")
async def register_response_middleware(_, __):
    """注册响应中间件"""
    for middleware in [func for func in dir(ResponseMiddleware) if func.endswith("middleware")]:
        server_app.register_middleware(getattr(ResponseMiddleware, middleware), "response")


@server_app.listener("before_server_stop")
async def server_shutdown(_, __):
    pass


if __name__ == '__main__':
    server_app.run(**config.SERVER_CONFIG)
