#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: __init__.py
Description: 独立工具文件夹, 该文件夹下的文件应具备不对其他任何自定义文件有依赖, 可以单独拿出使用的特性
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""

from .logger import error_logger
from .response import json_response

__all__ = ["json_response", "error_logger"]
