#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: pydantic_model
Description: Pydantic 模型，用于进行参数检查
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2021-09-08
"""
__all__ = ["TestDanticModel"]

from sanic_dantic import BaseModel, Field


class TestDanticModel(BaseModel):
    """测试参数检查模型"""
    test: int = Field(description="要过滤的id")


if __name__ == '__main__':
    print(TestDanticModel(**{"test": 1}))
