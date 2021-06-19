#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: config
Description: 基础配置文件, 封装了 DictConfig 类, 请勿更改此文件
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-04-28
"""

import os
from inspect import isfunction
from typing import Any
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DictConfig(dict):
    """
    封装的DictConfig 类, 请勿修改此类, 如需修改, 请在 config.py 中进行重写操作
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGGING_CONFIG = dict(
        version=1,
        disable_existing_loggers=True,
        loggers={
            "sanic.root": {"level": "INFO", "handlers": ["console", "info_file"]},
            "sanic.error": {
                "level": "INFO",
                "handlers": ["error_console", "error_file"],
                "propagate": True,
                "qualname": "sanic.error",
            },
            "sanic.access": {
                "level": "INFO",
                "handlers": ["access_console"],
                "propagate": True,
                "qualname": "sanic.access",
            },
        },
        handlers={
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": sys.stdout,
            },
            "error_console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": sys.stderr,
            },
            "access_console": {
                "class": "logging.StreamHandler",
                "formatter": "access",
                "stream": sys.stdout,
            },
            "info_file": {
                'level': "INFO",
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'generic',
                'filename': os.path.join(BASE_DIR, "logs", "info.log"),
                'when': "midnight",  # 切割日志的时间
                'backupCount': 7,  # 备份份数
                'encoding': 'utf-8'
            },
            "error_file": {
                'level': "INFO",
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'generic',
                'filename': os.path.join(BASE_DIR, "logs", "error.log"),
                'when': "midnight",  # 切割日志的时间
                'backupCount': 7,  # 备份份数
                'encoding': 'utf-8'
            },
        },
        formatters={
            "generic": {
                "format": "%(asctime)s [%(levelname)s] %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class": "logging.Formatter",
            },
            "access": {
                "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
                          + "%(request)s %(message)s %(status)d %(byte)d",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class": "logging.Formatter",
            },
        },
    )

    def __setattr__(self, key: str, value: Any) -> None:
        self.update({key: value})

    def __getattr__(self, key: str) -> Any:
        return self.get(key)

    def update_config(self, _config: Any) -> None:
        for key in dir(_config):
            var = getattr(_config, key)
            if not isfunction(var) and not key.startswith("_"):
                self.__setattr__(key, var)
