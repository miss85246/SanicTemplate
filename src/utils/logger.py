#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: exception
Description: 错误打印格式化
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2021-09-08
"""

import os
import traceback
from typing import Any

from sanic.log import error_logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def machining_exception(exception: Exception) -> list:
    """
    加工异常, 返回异常的行号以及文件路径
    :return: [(5, /scratches/scratch.py)]
    """
    return [(item.filename.split(BASE_DIR)[-1], item.lineno, item.line)
            for item in traceback.extract_tb(exception.__traceback__)
            if len(item.filename.split(BASE_DIR)) >= 2]


def error(msg: Any, exception: Exception = None, *args, **kwargs) -> None:
    """
    自定义 error 日志
    :param msg: 自定义信息
    :param exception: 错误类
    """
    if exception:
        exceptions = machining_exception(exception)
        stacks_msg = "\n".join([f"[错误堆栈]: [{trace[0]}] [line:{trace[1]}] [code]: {trace[-1]}" for trace in exceptions])
        msg = f"{msg}\n[错误原因]:{exception}\n{stacks_msg}"
    msg = msg + "\n" + "-" * 40 + "\n"
    error_logger.normal_error(msg, *args, **kwargs)


normal_error = getattr(error_logger, "error")
setattr(error_logger, "normal_error", normal_error)
setattr(error_logger, "error", error)
