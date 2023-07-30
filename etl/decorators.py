import time
from functools import wraps
import logging
from configs import app_config as config

logging.basicConfig(filename=config.log_filename, level=config.logging_level,
                    format='%(asctime)s  %(message)s')
logger = logging.getLogger(__name__)


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания
    (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            t = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    error_msg = f"Error connecting to DB: {error}"
                    logger.error(error_msg)

                if t < border_sleep_time:
                    t = start_sleep_time * factor
                else:
                    t = border_sleep_time

                time.sleep(t)

        return inner

    return func_wrapper
