import logging


def decorator_func(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logging.error(f"Error: {e}")
        except OSError as e:
            logging.error(f"Error : {e}")
    return wrapper

