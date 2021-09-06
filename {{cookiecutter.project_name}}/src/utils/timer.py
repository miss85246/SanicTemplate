from functools import wraps
from time import time

from sanic.log import logger


def timer():
    def decorator(function):
        @wraps(function)
        async def timer_function(*args, **kwargs):
            start_time = time()
            function(*args, **kwargs)
            end_time = time()
            cost_time = start_time - end_time
            logger.info(f"函数 {cost_time} 执行完毕，共耗时：{cost_time} 秒")

        return timer_function

    return decorator
