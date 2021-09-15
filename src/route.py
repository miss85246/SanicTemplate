#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: route.py
Description: 路由注册文件, 用于注册蓝图和其他路由
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2021-09-08
"""
from sanic.blueprints import Blueprint

from views import *

# 路由格式: version_prefix + version + url_prefix + URI definition

# 声明蓝图
test_bp = Blueprint("root", url_prefix="/", version=1, version_prefix="/api/v")

# 注册路由
test_bp.add_route(test_v1.TestView.as_view(), "/test")

# 声明蓝图组
server_bp = Blueprint.group(test_bp)
