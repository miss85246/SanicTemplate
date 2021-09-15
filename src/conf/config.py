#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: config
Description: 生产环境项目配置文件
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2021-09-08
"""

# 因为 ES 和 ArangoDB 不支持
# 尽量连接都使用 URI, URI 具体格式如下:
#      ArangoDB:   http://[host]:[port]  # python-arangodb 暂时不支持使用 http Authorization
#         Redis:   redis://[username]:[password]@[host]:[port]
#      DataBase:   mysql+aiomysql://[username]:[password]@[host]:[port]
#                  postgresql+asyncpg://[username]:[password]@[host]:[port]
#                  sqlite+aiosqlite://[username]:[password]@[host]:[port]
# ElasticSearch: http://[username]:[password]@[host]:[port]
#       MongoDB:   mongodb://[username]:[password]@[host]:[port]
from conf.baseConfig import BaseConfig


class ServerConfig(BaseConfig):
    """
    项目配置文件, 所有的配置都在此类下实现
    """

    # 设定错误返回格式为Json
    FALLBACK_ERROR_FORMAT = "json"
    # 运行配置
    SERVER_CONFIG = {"workers": 4, "access_log": False, "host": "0.0.0.0", "port": 5000, "debug": False}

    # ArangoDB 配置
    ARANGO_CONFIG = {
        "uris": "http://192.168.3.18:8529",
        "host_resolver": "roundrobin",  # random 或 roundrobin, 随机或顺序轮询, 不支持哨兵模式
        "database": "test",
        "username": "root",
        "password": "root"
    }
    # 数据库配置
    DB_CONFIG = {
        "uri": "mysql://192.168.3.18:3306",
        "datatype": "mysql",
        "username": "root",
        "password": "root",
        "database": "test",
        "pool_size": 8,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
        "echo": False,
        "migrate": False
    }
    # ElasticSearch 配置
    ES_CONFIG = {
        "uris": ["http://192.168.3.18:9200"],
        "username": "elastic",
        "password": "123456"
    }

    # KafkaConsumer 配置, 参考: https://aiokafka.readthedocs.io/en/stable/api.html#aiokafkaconsumer-class
    KAFKA_CONSUMER_CONFIG = {
        "topics": ["foo"],
        "uris": ["192.168.3.18:9092"],
    }

    # KafkaProducer 配置, 参考: https://aiokafka.readthedocs.io/en/stable/api.html#aiokafkaproducer-class
    KAFKA_PRODUCER_CONFIG = {
        "uris": ["192.168.3.18:9092"]
    }

    # MongoDB 配置
    MONGO_CONFIG = {
        "uri": "mongo://192.168.3.18:27017",
        "username": "root",
        "password": "root",
        "database": "test",
        "collection": "test",
        "minsize": 1,
        "maxsize": 10,
        "timeout": 10 * 1000
    }
    # Redis 配置
    REDIS_CONFIG = {
        "uri": "redis://192.168.3.18:6379",
        "db": 0,
        "password": None,
        "max_connections": 10,
        "decode_responses": True,
        "encoding": "utf-8"
    }
    # Sanic JWT 配置
    JWT_CONFIG = {
        "secret": "yCsxexdbYKCAIIeLvjqWSLHObMJnbwTQOVDykyXbFQRuTQMTxSVRMmDjlYhrNgVu",
        "algorithm": "HS512",
        "claim_aud": None,
        "claim_iat": True,
        "claim_iss": None,
        "claim_nbf": None,
        "claim_nbf_delta": 60 * 3 * 60,  # 过期时间
        "scopes_enabled": False  # 开启权限认证
    }
