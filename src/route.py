#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: route.py
Description: 路由注册文件, 用于注册蓝图和其他路由
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-16
"""
from views import *
from sanic.blueprints import Blueprint

# 声明蓝图
root_bp = Blueprint("root", url_prefix="/")

# 注册路由
root_bp.add_route(TestView.as_view(), "/test")

# 声明蓝图组
server_bp = Blueprint.group(root_bp)
