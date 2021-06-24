#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: config
Description: 生产环境项目配置文件
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-05-24
"""

from conf.baseConfig import BaseConfig


class ServerConfig(BaseConfig):
    """
    项目配置文件, 所有的配置都在此类下实现
    """

    # 设定错误返回格式为Json
    FALLBACK_ERROR_FORMAT = "json"

    # 运行配置
    SERVER_CONFIG = {"workers": 4, "access_log": False, "host": "0.0.0.0", "port": 5000, "debug": False}

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
    ES_CONFIG = {"nodes": [{"host": "localhost", "port": 9200}], "username": "elastic", "password": "123456"}

    # Redis 配置
    REDIS_CONFIG = {
        "host": "localhost",
        "port": "6379",
        # "password": "f66sU9iP",
        "database": 0,
        "minsize": 1,
        "maxsize": 10,
        "timeout": 10
    }

    # MongoDB 配置
    MONGO_CONFIG = {
        "host": "localhost",
        "port": "27017",
        "username": "root",
        "password": "root",
        "database": "test",
        "collection": "test",
        "minsize": 1,
        "maxsize": 10,
        "timeout": 10 * 1000
    }

    ARANGO_CONFIG = {
        "host": "localhost",
        "port": "8529",
        "database": "test",
        "username": "root",
        "password": "root"
    }
