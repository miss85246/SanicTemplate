#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: config
Description: 基础配置文件, 封装了 BaseConfig 类, 请勿更改此文件
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""

import os
import sys
from abc import ABCMeta


class BaseConfig(metaclass=ABCMeta):
    """
    DictConfig 抽象类, 如需修改, 请在 config.py 中进行重写
    """

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    LOGGING_CONFIG = dict(
        version=1,
        disable_existing_loggers=True,
        loggers={
            "sanic.root": {
                "level": "INFO",
                "handlers": ["console", "info_file"],
                "propagate": True,
                "qualname": "sanic.root",
            },
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
                "format": "%(asctime)s -[%(levelname)s][%(host)s]: %(request)s %(message)s %(status)d %(byte)d",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class": "logging.Formatter",
            },
        },
    )
