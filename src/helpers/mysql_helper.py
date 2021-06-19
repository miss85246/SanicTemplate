#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: mysql_helper
Description: MySQL 异步客户端
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-16
"""
import asyncio

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.orm import sessionmaker
from typing import Any
from models.sqlalchemy_model import Base, Test
from sanic.log import error_logger
from utils import *


class DBClient:
    """SQLAlchemy 异步封装, 用于实现数据库查询"""

    def __init__(self, db_type, host, port, user, passwd, database, **kwargs):
        engine_dict = {"mysql": "aiomysql", "postgresql": "asyncpg", "sqlite": "aiosqlite"}
        db, engine = db_type, engine_dict.get(db_type)
        self.engine = create_async_engine(
            f"{db}+{engine}://{user}:{passwd}@{host}:{port}/{database}",
            pool_size=kwargs.get("pool_size", 8),
            pool_recycle=kwargs.get("pool_recycle", 3600),
            pool_timeout=kwargs.get("pool_timeout", 10),
            pool_pre_ping=kwargs.get("pool_pre_ping", False),
            echo=kwargs.get("echo", False)
        )
        self.migrate = kwargs.get("migrate", False)
        self.async_session = None
        self.session = None

    async def session_init(self):
        """连接初始化"""
        if self.migrate:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
        if self.migrate:  # 该部分仅做示例使用, 实际使用时视情况自由修改
            async with self.session.begin() as session:
                session.add_all(
                    [Test(name="张三", age=11, sex="男"),
                     Test(name="李四", age=22, sex="男"),
                     Test(name="王五", age=33, sex="女"),
                     Test(name="赵六", age=44, sex="女")]
                )

    async def session_shutdown(self):
        await self.engine.dispose()

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

    async def example_func(self, filter_id: int):
        async with self.session() as session:
            try:
                res = await session.execute(select(Test).where(Test.id != filter_id))
                return self._res_to_dict(res, Test)
            except Exception as e:
                error_logger.error("查询Test出错", exception=e)
                await session.rollback()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    db_client = DBClient("mysql", "localhost", 3306, "root", "123456", "test", migrate=True)
    loop.run_until_complete(db_client.session_init())
    print(loop.run_until_complete(db_client.example_func()))
