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
import httpx
from aioarangodb import ArangoClient
from elasticsearch import AsyncElasticsearch
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models.sqlalchemy_model import Base


class AbstractArangoDBClient(metaclass=ABCMeta):

    def __init__(self, host: str, port: int, database: str, username: str, password: str):
        self.connection = None
        self.client = None
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password

    async def __async_init__(self):
        self.connection = ArangoClient(hosts="http" + f"://{self.host}:{self.port}")
        self.client = await self.connection.db(name=self.database, username=self.username, password=self.password)
        return self

    def __await__(self):
        return self.__async_init__().__await__()

    async def close(self):
        await self.connection.close()


class AbstractDBClient(metaclass=ABCMeta):

    def __init__(self, db_type: str, host: str, port: int, username: str, password: str, database: str, **kwargs):
        engine_dict = {"mysql": "aiomysql", "postgresql": "asyncpg", "sqlite": "aiosqlite"}
        self.db = db_type
        self.engine = engine_dict.get(db_type)
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
            await self.session_begin()

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

    async def session_begin(self):
        async with self.session.begin() as session:
            pass

    async def close(self):
        await self.engine.dispose()


class AbstractEsClient(metaclass=ABCMeta):

    def __init__(self, host: str = None, port: int = None, username: str = "", password: str = "", **kwargs):
        if host and port and not kwargs.get("nodes"):
            self.nodes = [{"host": host, "port": port}]
        else:
            nodes = kwargs.get("nodes")
            if not isinstance(nodes, Iterable):
                raise TypeError("nodes argument must be Iterable, example: [{'host':'localhost', 'port':9200}]")
            for node in nodes:
                if not node.get("host") or not node.get("port"):
                    raise ValueError("host and port must in node, example: {'host':'localhost', 'port':9200}")
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
        await self.session.end_session()


class AbstractRedisClient(metaclass=ABCMeta):

    def __init__(self, host: str = None, port: int = None, password: str = None, mode: str = "normal", **kwargs):
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


class AbstractHttpClient(metaclass=ABCMeta):
    def __init__(self, timeout=10, retry=5, status_retry=True):
        self.session = httpx.AsyncClient()
        self.retry = retry
        self.status_retry = status_retry
        self.timeout = timeout

    async def __async__init__(self):
        return self

    def __await__(self):
        return self.__async__init__().__await__()

    async def send(self, method: str, *args: Any, **kwargs: Any) -> httpx.Response:
        for sent_times in range(self.retry):
            try:
                request = getattr(self.session, method.lower(), self.session.get)
                result = await request(*args, **kwargs, timeout=self.timeout)
                if self.return_rules(sent_times, result):
                    return result
            except httpx.TimeoutException:
                self.timeout_rules()
        raise httpx.RequestError(f"All Request Failed in {self.retry} Times")

    def return_rules(self, sent_times: int, result: httpx.Response) -> bool:
        if result.status_code == 200 and sent_times < self.retry:
            return True

    def timeout_rules(self, *args, **kwargs) -> Any:
        pass

    async def get(self, *args: Any, **kwargs: Any) -> httpx.Response:
        return await self.send("get", *args, **kwargs)

    async def post(self, *args: Any, **kwargs: Any) -> httpx.Response:
        return await self.send("post", *args, **kwargs)

    async def put(self, *args: Any, **kwargs: Any) -> httpx.Response:
        return await self.send("put", *args, **kwargs)

    async def head(self, *args: Any, **kwargs: Any) -> httpx.Response:
        return await self.send("head", *args, **kwargs)

    async def options(self, *args: Any, **kwargs: Any) -> httpx.Response:
        return await self.send("options", *args, **kwargs)

    async def close(self):
        await self.session.aclose()
