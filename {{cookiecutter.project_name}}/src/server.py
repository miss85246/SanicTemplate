#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: server.py
Description: Server 文件, 用于启动服务
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""

from sanic import Sanic
# cookiecutter_flag {%- if cookiecutter.enable_jwt == 'True'%}
from sanic_jwt import Initialize

from authorization import Authentication
# cookiecutter_flag {%- endif %}
from conf import config
# cookiecutter_flag {%- if cookiecutter.enable_arangodb == 'True' %}
from helpers import ArangoDBClient
# cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_database == 'True' %}
from helpers import DBClient
# cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_elasticsearch == 'True' %}
from helpers import EsClient
# cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_httpx == 'True' %}
from helpers import HttpxClient
# cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_mongodb == 'True' %}
from helpers import MongoClient
# cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_redis == 'True' %}
from helpers import RedisClient
# cookiecutter_flag {%- endif %}
from middlewares import RequestMiddleware, ResponseMiddleware
from route import server_bp

server_app = Sanic("server", log_config=config.LOGGING_CONFIG)
server_app.config.update_config(config)
# cookiecutter_flag {%- if cookiecutter.enable_jwt == 'True' %}
auth = Authentication(config.JWT_CONFIG)
Initialize(server_app, **auth.config)
# cookiecutter_flag {%- endif %}
server_app.blueprint(server_bp)


@server_app.listener("after_server_start")
async def server_init(_, __):
    """用于初始化各类存储管理类, 可以按需进行修改"""
    # cookiecutter_flag {%- if cookiecutter.enable_arangodb == 'True' %}
    server_app.ctx.arangodb = await ArangoDBClient(**server_app.config.ARANGO_CONFIG)
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_database == 'True' %}
    server_app.ctx.database = await DBClient(**server_app.config.DB_CONFIG)
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_elasticsearch == 'True' %}
    server_app.ctx.elasticsearch = await EsClient(**server_app.config.ES_CONFIG)
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_httpx == 'True' %}
    server_app.ctx.httpx = await HttpxClient()
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_mongodb == 'True' %}
    server_app.ctx.mongo = await MongoClient(**server_app.config.MONGO_CONFIG)
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_redis == 'True' %}
    server_app.ctx.redis = await RedisClient(**server_app.config.REDIS_CONFIG)
    # cookiecutter_flag {%- endif %}


@server_app.listener("after_server_start")
async def register_middleware(_, __):
    """注册请求/响应中间件"""
    [server_app.register_middleware(middleware, "request") for middleware in RequestMiddleware().middlewares]
    [server_app.register_middleware(middleware, "response") for middleware in ResponseMiddleware().middlewares]


@server_app.listener("before_server_stop")
async def server_shutdown(_, __):
    """注销初始化时各类存储管理类, 可以按需进行修改"""
    # cookiecutter_flag {%- if cookiecutter.enable_arangodb == 'True' %}
    await server_app.ctx.arangodb.close()
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_database == 'True' %}
    await server_app.ctx.database.close()
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_elasticsearch == 'True' %}
    await server_app.ctx.elasticsearch.close()
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_httpx == 'True' %}
    await server_app.ctx.httpx.close()
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_mongodb == 'True' %}
    await server_app.ctx.mongo.close()
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_redis == 'True' %}
    await server_app.ctx.redis.close()
    # cookiecutter_flag {%- endif %}


if __name__ == '__main__':
    server_app.run(**config.SERVER_CONFIG)
