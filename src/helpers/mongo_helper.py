#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: mongo_helper
Description: MongoDB 异步客户端
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-18
"""

from motor.motor_asyncio import AsyncIOMotorClientSession


class MongoClient:
    def __init__(self):
        self.mongo = AsyncIOMotorClientSession()
