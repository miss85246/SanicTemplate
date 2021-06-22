#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: sqlalchemy_model
Description: 
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-06-17
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """
    基础抽象模型
    """
    __abstract__ = True
    _attrs_dict = {}
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), server_default=func.now())
    delete_time = Column(DateTime(timezone=True), server_default=None)


class Test(BaseModel):
    """
    测试模型
    """
    __tablename__ = "test"
    name = Column(String(16), unique=True, nullable=False, index=True)
    age = Column(Integer)
    sex = Column(String(1))
