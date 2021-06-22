#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: __init__.py
Description: 配置文件夹, 包含 config 以及 dev_config, 切换时修改该文件夹下的 Develop 即可
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-04-28
"""

Develop = True

if not Develop:
    from .config import ServerConfig as config
else:
    from .dev_config import ServerConfig as config
