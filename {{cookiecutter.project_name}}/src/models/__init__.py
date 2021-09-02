#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: __init__.py
Description: 
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""

from .pydantic_model import *
# cookiecutter_flag {%- if cookiecutter.enable_database == 'True' %}
from .sqlalchemy_model import *
# cookiecutter_flag {%- endif %}
