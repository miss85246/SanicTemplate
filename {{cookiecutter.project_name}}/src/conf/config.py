#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: config
Description: 生产环境项目配置文件
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
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
        "workers": int("{{cookiecutter.server_workers_count}}"),
        "access_log": False,
        "host": "{{cookiecutter.server_bind_host}}",
        "port": int("{{cookiecutter.server_bind_port}}"),
        "debug": False
    }

    # cookiecutter_flag {%- if cookiecutter.enable_arangodb == 'True' %}
    # ArangoDB 配置
    ARANGO_CONFIG = {
        "hosts": ["http://localhost:8529"],
        "host_resolver": "roundrobin",  # random
        "database": "test",
        "username": "root",
        "password": "root"
    }
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_database == 'True' %}
    # 数据库配置
    DB_CONFIG = {
        "db_type": "{{cookiecutter.db_type}}",
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
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_elasticsearch == 'True' %}
    # ElasticSearch 配置
    ES_CONFIG = {
        "nodes": ["http://localhost:9200"],
        "username": "elastic",
        "password": "123456"
    }
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_mongodb == 'True' %}
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
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_redis == 'True' %}
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
    # cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_jwt == 'True' %}
    # Sanic JWT 配置
    JWT_CONFIG = {
        "secret": "{{ random_ascii_string(64) }}",
        "algorithm": "HS512",
        "claim_aud": None,
        "claim_iat": True,
        "claim_iss": None,
        "claim_nbf": None,
        "claim_nbf_delta": 60 * 3 * 60,  # 过期时间
        "scopes_enabled": False  # 开启权限认证
    }
    # cookiecutter_flag {%- endif %}
