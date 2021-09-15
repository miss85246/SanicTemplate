#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: config
Description: 生产环境项目配置文件
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2021-09-08
"""

from conf.baseConfig import BaseConfig


class ServerConfig(BaseConfig):
    """
    项目配置文件, 所有的配置都在此类下实现
    """

    # 设定错误返回格式为Json
    FALLBACK_ERROR_FORMAT = "json"

    # 运行配置
    SERVER_CONFIG = {
        "workers": int("4"),
        "access_log": False,
        "host": "0.0.0.0",
        "port": int("5000"),
        "debug": False
    }

    # ArangoDB 配置
    ARANGO_CONFIG = {
        "hosts": ["http://localhost:8529"],
        "host_resolver": "roundrobin",  # random
        "database": "test",
        "username": "root",
        "password": "root"
    }
    # 数据库配置
    DB_CONFIG = {
        "db_type": "mysql",
        "host": "localhost",
        "port": 3306,
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
        "nodes": ["http://localhost:9200"],
        "username": "elastic",
        "password": "123456"
    }

    # KafkaConsumer 配置, 参考: https://aiokafka.readthedocs.io/en/stable/api.html#aiokafkaconsumer-class
    KAFKA_CONSUMER_CONFIG = {
        "topics": ["foo"],
        "uris": ["localhost:9092"],
    }

    # KafkaProducer 配置, 参考: https://aiokafka.readthedocs.io/en/stable/api.html#aiokafkaproducer-class
    KAFKA_PRODUCER_CONFIG = {
        "uris": ["localhost:9092"]
    }

    # MongoDB 配置
    MONGO_CONFIG = {
        "host": "localhost",
        "port": 27017,
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
        "host": "localhost",
        "port": 6379,
        "password": "f66sU9iP",
        "database": 0,
        "minsize": 1,
        "maxsize": 10,
        "timeout": 10
    }
    # Sanic JWT 配置
    JWT_CONFIG = {
        "secret": "uoayKlcorQwbyaEIKrPgVHLwZZAzZzMRNuxKWJiIvfOCLArWIiogRrlxVrSqcWhC",
        "algorithm": "HS512",
        "claim_aud": None,
        "claim_iat": True,
        "claim_iss": None,
        "claim_nbf": None,
        "claim_nbf_delta": 60 * 3 * 60,  # 过期时间
        "scopes_enabled": False  # 开启权限认证
    }
