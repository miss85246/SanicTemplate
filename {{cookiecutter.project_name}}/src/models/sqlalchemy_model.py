# cookiecutter_flag {%- if cookiecutter.enable_database == 'True' %}
# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: sqlalchemy_model
Description: SQLAlchemy 模型， 用于进行数据库关系映射
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

__all__ = ["Base", "Test"]

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
# cookiecutter_flag {%- endif %}
