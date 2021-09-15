from functools import wraps
from time import time

from sanic.log import logger


def timer(name: str = ""):
    def decorator(function):
        @wraps(function)
        async def timer_function(*args, **kwargs):
            start_time = time()
            res = await function(*args, **kwargs)
            end_time = time()
            cost_time = end_time - start_time
            logger.info(f"函数 {name or function.__name__} 执行完毕，共耗时：{cost_time} 秒")
            return res

        return timer_function

    return decorator
