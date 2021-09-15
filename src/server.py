#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: server.py
Description: Server 文件, 用于启动服务
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2021-09-08
"""

from sanic import Sanic
from sanic_jwt import Initialize

from authorization import Authentication
from conf import config
from helpers import ArangoDBClient
from helpers import DBClient
from helpers import EsClient
from helpers import HttpxClient
from helpers import MongoClient
from helpers import RedisClient
from middlewares import RequestMiddleware, ResponseMiddleware
from route import server_bp

server_app = Sanic("server", log_config=config.LOGGING_CONFIG)
server_app.config.update_config(config)
auth = Authentication(config.JWT_CONFIG)
Initialize(server_app, **auth.config)
server_app.blueprint(server_bp)


@server_app.listener("after_server_start")
async def server_init(_, __):
    """用于初始化各类存储管理类, 可以按需进行修改"""
    server_app.ctx.arangodb = await ArangoDBClient(**server_app.config.ARANGO_CONFIG)
    server_app.ctx.database = await DBClient(**server_app.config.DB_CONFIG)
    server_app.ctx.elasticsearch = await EsClient(**server_app.config.ES_CONFIG)
    server_app.ctx.httpx = await HttpxClient()
    server_app.ctx.mongo = await MongoClient(**server_app.config.MONGO_CONFIG)
    server_app.ctx.redis = await RedisClient(**server_app.config.REDIS_CONFIG)


@server_app.listener("after_server_start")
async def register_middleware(_, __):
    """注册请求/响应中间件"""
    [server_app.register_middleware(middleware, "request") for middleware in RequestMiddleware().middlewares]
    [server_app.register_middleware(middleware, "response") for middleware in ResponseMiddleware().middlewares]


@server_app.listener("before_server_stop")
async def server_shutdown(_, __):
    """注销初始化时各类存储管理类, 可以按需进行修改"""
    await server_app.ctx.arangodb.close()
    await server_app.ctx.database.close()
    await server_app.ctx.elasticsearch.close()
    await server_app.ctx.httpx.close()
    await server_app.ctx.mongo.close()
    await server_app.ctx.redis.close()


if __name__ == '__main__':
    server_app.run(**config.SERVER_CONFIG)
