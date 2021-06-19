#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: pydantic_model
Description: 用于进行参数检查
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-05-24
"""

from sanic_dantic import BaseModel, Field


class TestDanticModel(BaseModel):
    """测试参数检查模型"""
    test: int = Field(description="要过滤的id")
