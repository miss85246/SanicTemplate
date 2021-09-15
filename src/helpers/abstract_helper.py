# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: abstract_helper
Description: 各类 helper 抽象客户端, 对应的 helper 继承该文件下的对应类,  其他文件下的help类只需要关注实际的业务需求即可
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2021-09-08
"""

from abc import ABCMeta
from typing import Iterable, Any

import aioredis
import httpx
from aioarangodb import ArangoClient
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aioredis import sentinel
from elasticsearch import AsyncElasticsearch
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models.sqlalchemy_model import Base


class AbstractArangoDBClient(metaclass=ABCMeta):
    """
    ArangoDB 抽象类，封装了 aioarangodb 异步方法
    """

    def __init__(self, uris: [str], database: str, username: str, password: str, host_resolver: str):
        """
        初始化，仅用于参数的声明

        :param uris: 数据库连接 uri
        :param database: 数据库名称
        :param username: 用户名
        :param password: 密码
        :return: None
        """
        self.connection = None
        self.client = None
        self.uris = uris
        self.host_resolver = host_resolver
        self.database = database
        self.username = username
        self.password = password

    async def __async_init__(self):
        """
        异步初始化函数，真正的初始化是在此完成的

        :return: self
        """
        self.connection = ArangoClient(hosts=self.uris, host_resolver=self.host_resolver)
        self.client = await self.connection.db(self.database, username=self.username, password=self.password)
        return self

    def __await__(self):
        """
        异步方法，用于异步实例化

        :return: self
        """
        return self.__async_init__().__await__()

    async def close(self):
        """
        关闭方法，用于关闭数据库连接

        :return: None
        """
        await self.connection.close()


class AbstractDBClient(metaclass=ABCMeta):

    def __init__(self, uri: str, datatype: str, username: str, password: str, database: str, **kwargs):
        engine_dict = {"mysql": "aiomysql", "postgresql": "asyncpg", "sqlite": "aiosqlite"}
        self.datatype = datatype
        self.engine = engine_dict.get(datatype)
        self.pool_size = kwargs.get("pool_size", 8)
        self.pool_recycle = kwargs.get("pool_recycle", 3600)
        self.pool_timeout = kwargs.get("pool_timeout", 10)
        self.pool_pre_ping = kwargs.get("pool_pre_ping", False)
        self.echo = kwargs.get("echo", False)
        self.migrate = kwargs.get("migrate", False)
        host, port = uri.split("@")[-1].split("/")[-1].split(":")
        self.uri = f"{datatype}+{self.engine}://{username}:{password}@{host}:{port}/{database}"
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

    def __init__(self, uris: [str], username: str = "", password: str = "", **kwargs):
        if not isinstance(uris, Iterable):
            raise ValueError("nodes argument must be Iterable, example: ['http://localhost:9200']")
        self.uris = uris
        self.client = None
        self.username = username
        self.password = password
        self.kwargs = kwargs

    async def __async__init__(self):
        self.client = AsyncElasticsearch(self.uris, http_auth=(self.username, self.password), **self.kwargs)
        return self

    def __await__(self):
        return self.__async__init__().__await__()

    async def close(self):
        await self.client.close()


class AbstractHttpxClient(metaclass=ABCMeta):
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


class AbstractKafkaProducerClient(metaclass=ABCMeta):

    def __init__(self, uris: [str], **kwargs):
        self.producer = AIOKafkaProducer(bootstrap_servers=uris, **kwargs)
        self.uris = uris

    async def __async_init__(self):
        await self.producer.start()

    def __await__(self):
        return self.__async_init__().__await__()

    async def close(self):
        await self.producer.stop()


class AbstractKafkaConsumerClient(metaclass=ABCMeta):
    def __init__(self, topics: [str], uris: [str], **kwargs):
        self.topics = topics
        self.uris = uris
        self.consumer = AIOKafkaConsumer(*topics, bootstrap_servers=uris, **kwargs)

    async def __async_init__(self):
        await self.consumer.start()

    def __await__(self):
        return self.__async_init__().__await__()

    async def close(self):
        await self.consumer.stop()


class AbstractMongoClient(metaclass=ABCMeta):

    def __init__(self, uri: str, username: str = None, password: str = None, **kwargs):
        self.username = username
        self.password = password
        self.database = kwargs.get("database", None)
        self.collection = kwargs.get("collection", None)
        self.maxsize = kwargs.get("maxsize", 10)
        self.minsize = kwargs.get("minsize", 1)
        self.authSource = kwargs.get("authSource", "admin")
        self.timeout = kwargs.get("timeout", 10)
        print()
        host, port = uri.split("@")[-1].split("/")[-1].split(":")
        self.uri = f"mongodb://{self.username}:{self.password}@{host}:{port}/{self.database}"
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

    def __init__(self, uri: str = None, password: str = None, mode: str = "normal", **kwargs):
        self.redis = None
        self.sentinel = None
        self.kwargs = kwargs
        self.uri = uri
        self.mode = mode
        self.password = None or password
        self.database = kwargs.get("database")
        self.kwargs = kwargs

    async def __async__init__(self):
        if self.mode == "normal":
            pool = aioredis.ConnectionPool.from_url(self.uri, password=self.password, **self.kwargs)
            self.redis = aioredis.Redis(connection_pool=pool)
        elif self.mode == "sentinel":
            self.sentinel = sentinel.Sentinel(self.uri, password=self.password, **self.kwargs)
            self.redis = self.sentinel.master_for("redis")
        else:
            raise ValueError("mode must one of normal / sentinel")
        return self

    def __await__(self):
        return self.__async__init__().__await__()

    async def close(self):
        await self.redis.close()
