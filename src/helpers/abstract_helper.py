#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: abstract_helper
Description: 各类 helper 抽象客户端, 对应的 helper 继承该文件下的对应类,  其他文件下的help类只需要关注实际的业务需求即可
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-23
"""

from abc import ABCMeta
from typing import Iterable, Any

import aioredis
from aioarangodb import ArangoClient
from elasticsearch import AsyncElasticsearch
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models.sqlalchemy_model import Base


class AbstractArangoDBClient(metaclass=ABCMeta):

    def __init__(self, host: str, port: str, database: str, username: str, password: str, **kwargs):
        self.client = None
        self._host = host
        self._port = port
        self._database = database
        self._username = username
        self._password = password

    async def __async_init__(self):
        client = ArangoClient(hosts=f"http://{self._host}:{self._port}")
        self.client = await client.db(name=self._database, username=self._username, password=self._password)
        return self

    def __await__(self):
        return self.__async_init__().__await__()

    async def close(self):
        await self.client.close()


class AbstractDBClient(metaclass=ABCMeta):

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
                pass

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

    async def close(self):
        await self.engine.dispose()


class AbstractEsClient(metaclass=ABCMeta):

    def __init__(self, host: str = None, port: str = None, username: str = "", password: str = "", **kwargs):
        if host and port and not kwargs.get("nodes"):
            self.nodes = [{"host": host, "port": port}]
        else:
            nodes = kwargs.get("nodes")
            if not isinstance(nodes, Iterable):
                raise TypeError("nodes argument must be Iterable, example: [{'host':'localhost', 'port':'9200'}]")
            for node in nodes:
                if not node.get("host") or not node.get("port"):
                    raise ValueError("host and port must in node")
            self.nodes = nodes
        self.client = None
        self.username = username
        self.password = password
        self.kwargs = kwargs

    async def __async__init__(self):
        self.client = AsyncElasticsearch(self.nodes, http_auth=(self.username, self.password), **self.kwargs)
        return self

    def __await__(self):
        return self.__async__init__().__await__()

    async def close(self):
        await self.client.close()


class AbstractMongoClient(metaclass=ABCMeta):
    """抽象类, 封装了 MongoDB 初始化, 请勿在此类上进行修改"""

    def __init__(self, host: str, port: int, username: str = None, password: str = None, **kwargs):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = kwargs.get("database", None)
        self.collection = kwargs.get("collection", None)
        self.maxsize = kwargs.get("maxsize", 10)
        self.minsize = kwargs.get("minsize", 1)
        self.authSource = kwargs.get("authSource", "admin")
        self.timeout = kwargs.get("timeout", 10)
        self.uri = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.uri = self.uri + f"?authSource={self.authSource}"
        self.mongo = AsyncIOMotorClient(self.uri,
                                        maxPoolSize=self.maxsize,
                                        minPoolSize=self.minsize,
                                        waitQueueTimeoutMS=self.timeout)
        self.session = None

    async def __async__init__(self):
        self.database = self.mongo[self.database] if self.database else None
        self.collection = self.database[self.collection] if self.database and self.collection else None
        self.session = await self.mongo.start_session()
        return self

    def __await__(self):
        return self.__async__init__().__await__()

    async def close(self):
        await self.session.close()


class AbstractRedisClient(metaclass=ABCMeta):

    def __init__(self, host: str = None, port: str = None, password: str = None, mode: str = "normal", **kwargs):
        self.redis = None
        self.kwargs = kwargs
        self.mode = mode
        self.nodes = kwargs.get("nodes", [(host, port)])
        self.node_size = len(self.nodes)
        self.password = None or password
        self.database = kwargs.pop("database", 0)
        self.timeout = kwargs.pop("timeout", 10)
        self.minsize = kwargs.pop("minsize", 1)
        self.maxsize = kwargs.pop("maxsize", 10)
        self.kwargs = kwargs

    async def __async__init__(self):
        self.redis = await aioredis.create_redis_pool(f"redis://{self.nodes[0][0]}:{self.nodes[0][1]}",
                                                      db=self.database,
                                                      password=self.password,
                                                      maxsize=self.maxsize,
                                                      minsize=self.minsize,
                                                      timeout=self.timeout,
                                                      **self.kwargs)
        return self

    def __await__(self):
        return self.__async__init__().__await__()

    async def close(self):
        self.redis.close()