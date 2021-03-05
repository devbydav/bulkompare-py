import logging
from time import perf_counter

logger = logging.getLogger(__name__)


def log_time_it(func):
    def timed(*args, **kw):
        t0 = perf_counter()
        res = func(*args, **kw)
        t1 = perf_counter()
        logger.debug(f"{func.__name__} done (in {round(t1-t0, 2)}s)")
        return res
    return timed
