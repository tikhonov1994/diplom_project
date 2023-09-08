import logging
from functools import wraps
from time import sleep


def backoff(exceptions: type | tuple[type, ...], start_sleep_time=0.1, factor=2, border_sleep_time=10, max_retries=10):
    """
    Декоратор, перезапускающий обернутую функцию при возникновении в ней определенных типов исключений.
    Интервал перезапуска вычисляется по формуле:
    wait_time = min(start_sleep_time * factor ** iteration, border_sleep_time)
    Здесь iteration - номер попытки перезапуска.
    :param exceptions: кортеж обрабатываемых исключений
    :param start_sleep_time: стартовый интервал перезапуска
    :param factor: основание степени из формулы показательной функции, по которой вычистяется интервал перезапуска.
    :param border_sleep_time: максимальная величина интервала перезапуска.
    :param max_retries: максимальное количество попыток, после которого декоратор вернет ConnectionError.
    Если значение установлено на 0, то количество попыток не ограничено.
    """

    def func_wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            iteration = 1
            wait_time = start_sleep_time
            while True:
                if max_retries != 0 and iteration > max_retries:
                    _msg = f'Failed to connect to the service after {max_retries} attempts, terminating..'
                    logging.critical(_msg)
                    raise ConnectionError(_msg)
                try:
                    results = func(*args, **kwargs)
                    return results
                except exceptions as exc:
                    logging.warning('\'%s\' exception raised on \'%s\' call, retry in %.2f s..',
                                    exc.__class__.__name__, func.__qualname__, wait_time)
                sleep(wait_time)
                iteration += 1
                wait_time = min(start_sleep_time * factor ** iteration, border_sleep_time)

        return inner

    return func_wrapper
