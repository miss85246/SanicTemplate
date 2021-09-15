# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: mysql_helper
Description: MySQL 异步客户端， 使用 SQLAlchemy 1.4.1 +
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2021-09-08
"""
import asyncio

from sqlalchemy.future import select

from conf import config
from helpers.abstract_helper import AbstractDBClient
from models.sqlalchemy_model import Test
from utils import error_logger


class DBClient(AbstractDBClient):

    def __init__(self, uri: str, datatype: str, username: str, password: str, database: str, **kwargs):
        super().__init__(uri, datatype, username, password, database, **kwargs)

    async def example_func(self, filter_id: int):
        async with self.session() as session:
            try:
                res = await session.execute(select(Test).where(Test.id != filter_id))
                return self._res_to_dict(res, Test)
            except Exception as e:
                error_logger.error("DBClient 查询 example_func 出错", exception=e)
                await session.rollback()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    db_client = loop.run_until_complete(DBClient(**config.DB_CONFIG))
    print(loop.run_until_complete(db_client.example_func(1)))
    loop.run_until_complete(db_client.close())
