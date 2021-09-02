# cookiecutter_flag {%- if cookiecutter.enable_helpers == 'True' %}
# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: __init__.py
Description: 初始化导入文件
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""

# cookiecutter_flag {%- if cookiecutter.enable_arangodb == 'True' %}
from .arangodb_helper import ArangoDBClient
# cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_database == 'True' %}
from .databased_helper import DBClient
# cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_elasticsearch == 'True' %}
from .es_helper import EsClient
# cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_httpx == 'True' %}
from .httpx_helper import HttpxClient
# cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_mongodb == 'True' %}
from .mongo_helper import MongoClient
# cookiecutter_flag {%- endif %} {%- if cookiecutter.enable_redis == 'True' %}
from .redis_helper import RedisClient
# cookiecutter_flag {%- endif %} {%- endif %}
