#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: mysql_helper
Description: MySQL 异步客户端， 使用 SQLAlchemy 1.4.1 +
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-16
"""
import asyncio
from typing import Any

from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from models.sqlalchemy_model import Base, Test
from utils import error_logger
from conf import config


class AbstractDBClient:

    def __init__(self, db_type: str, host: str, port: int, username: str, password: str, database: str, **kwargs):
        engine_dict = {"mysql": "aiomysql", "postgresql": "asyncpg", "sqlite": "aiosqlite"}
        self.db = db_type
        self.engine = engine_dict.get(db_type)
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.pool_size = kwargs.get("pool_size", 8)
        self.pool_recycle = kwargs.get("pool_recycle", 3600)
        self.pool_timeout = kwargs.get("pool_timeout", 10)
        self.pool_pre_ping = kwargs.get("pool_pre_ping", False)
        self.echo = kwargs.get("echo", False)
        self.migrate = kwargs.get("migrate", False)
        self.uri = f"{db_type}+{self.engine}://{username}:{password}@{host}:{port}/{database}"
        self.engine = None
        self.session = None

    async def __async__init__(self):
        self.engine = create_async_engine(self.uri,
                                          pool_size=self.pool_size,
                                          pool_recycle=self.pool_recycle,
                                          pool_timeout=self.pool_timeout,
                                          pool_pre_ping=self.pool_pre_ping,
                                          echo=self.echo)

        if self.migrate:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        if self.migrate:
            async with self.session.begin() as session:
                session.add_all([
                    Test(name="张三", age=11, sex="男"),
                    Test(name="李四", age=22, sex="男"),
                    Test(name="王五", age=33, sex="女"),
                    Test(name="赵六", age=44, sex="女")
                ])

        return self

    def __await__(self):
        return self.__async__init__().__await__()

    @staticmethod
    def _res_to_dict(res: ChunkedIteratorResult, model: Any = None):
        """响应结果转换成字典函数"""
        result = []
        for item in res:
            if list(item.keys()) == [model.__name__]:
                for tem in item:
                    result.append({key: value for key, value in tem.__dict__.items() if key != "_sa_instance_state"})
            else:
                result.append(item.__getattribute__("_asdict")())
        return result


class DBClient(AbstractDBClient):

    def __init__(self, db_type: str, host: str, port: int, username: str, password: str, database: str, **kwargs):
        super().__init__(db_type, host, port, username, password, database, **kwargs)

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
