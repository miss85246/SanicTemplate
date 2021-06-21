#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: config
Description: 
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-05-24
"""

from .baseConfig import DictConfig


class ServerConfig(DictConfig):
    """
    项目配置文件, 所有的配置都在此类下实现
    """
    FALLBACK_ERROR_FORMAT = "json"  # 设定错误返回格式为Json

    SERVER_CONFIG = {
        "workers": 1,
        "access_log": False,
        "host": "127.0.0.1",
        "port": 5000,
        "debug": False
    }

    DB_CONFIG = {
        "db_type": "mysql",
        "host": "192.168.3.128",
        "port": 3306,
        "user": "root",
        "passwd": "root",
        "database": "test",
        "pool_size": 8,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
        "echo": False,
        "migrate": False

    }

    ES_CONFIG = {
        "nodes": [
            {"host": "192.168.3.128", "port": "9200"}
        ],
        "username": "elastic",
        "password": "123456"
    }


config = ServerConfig

if __name__ == '__main__':
    print(ServerConfig.LOGGING_CONFIG)
