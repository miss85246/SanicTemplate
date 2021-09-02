#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: __init__.py
Description: 配置文件夹, 包含 config 以及 dev_config, 切换时修改该文件下的 Develop 即可
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""

Develop = True

if not Develop:
    from .config import ServerConfig as config
else:
    from .dev_config import ServerConfig as config
