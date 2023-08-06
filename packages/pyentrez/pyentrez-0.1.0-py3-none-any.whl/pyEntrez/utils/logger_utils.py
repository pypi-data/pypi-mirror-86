import functools
from loguru import logger

def logger_wraps(*, entry=True, exit=True, level="DEBUG"):

    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1,colors=True)
            if entry:
                logger_.log(level, f"<m><l>Entering '{name}'</></>")
            result = func(*args, **kwargs)
            if exit:
                logger_.log(level, f"<m><l>Exiting '{name}' (result={result})</></>")
            return result

        return wrapped

    return wrapper