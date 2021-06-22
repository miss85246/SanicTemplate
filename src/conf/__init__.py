#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: __init__.py
Description: 
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-04-28
"""

Develop = True

if not Develop:
    from .config import config
else:
    from .dev_config import config
