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
from helpers import DBClient, EsClient, RedisClient, RequestClient, ArangoDBClient, MongoClient
from middlewares import RequestMiddleware, ResponseMiddleware
from route import server_bp

server_app = Sanic("server", log_config=config.LOGGING_CONFIG)
server_app.config.update_config(config)
server_app.blueprint(server_bp)


@server_app.listener("after_server_start")
async def server_init(_, __):
    """用于初始化各类存储管理类, 可以按需进行修改"""
    server_app.ctx.database = await DBClient(**server_app.config.DB_CONFIG)
    server_app.ctx.es = await EsClient(**server_app.config.ES_CONFIG)
    server_app.ctx.redis = await RedisClient(**server_app.config.REDIS_CONFIG)
    server_app.ctx.request = RequestClient()
    server_app.ctx.arangodb = await ArangoDBClient(**server_app.config.ARANGO_CONFIG)
    server_app.ctx.mongo = await MongoClient(**server_app.config.MONGO_CONFIG)


@server_app.listener("after_server_start")
async def register_middleware(_, __):
    """注册请求/响应中间件"""
    [server_app.register_middleware(middleware, "request") for middleware in RequestMiddleware().middlewares]
    [server_app.register_middleware(middleware, "response") for middleware in ResponseMiddleware().middlewares]


@server_app.listener("before_server_stop")
async def server_shutdown(_, __):
    """注销初始化时各类存储管理类, 可以按需进行修改"""
    await server_app.ctx.database.close()
    await server_app.ctx.es.close()
    await server_app.ctx.redis.close()
    await server_app.ctx.arangodb.close()
    await server_app.ctx.mongo.close()


if __name__ == '__main__':
    server_app.run(**config.SERVER_CONFIG)
