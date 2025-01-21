import logging
from functools import wraps


def decorator_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logging.error(f"Error: {e}")
        except OSError as e:
            logging.error(f"Error : {e}")
        return func(*args, **kwargs)

    return wrapper
